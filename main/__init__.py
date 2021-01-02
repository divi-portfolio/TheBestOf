from flask import Flask, render_template, url_for, jsonify,request, Response, redirect, session
from .Spotipy_PlaylistMiner import keyWordPlaylist, get_playlist_tracks, get_tracks_from_all_playlists, get_unique_tracks_from_all_tracks,create_playlist_add_tracks, create_sp
import sqlite3, requests, spotipy
from .generate_codes import create_code_verifier_challenge

try:
    from .playlists_created_db import create_tables, playlists_created
    
except:
    from playlists_created_db import create_tables, playlists_created
    

app = Flask(__name__) ### get name of module 

global playlists
global playlists_dict
global all_tracks
global sp

#debugging purposes
if __name__ == '__main__':
    app.run( 'localhost',debug = True)

### FLASK SESSION
from flask import session
from flask_session import Session 

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
##SESSION_PERMANENT = 'FALSE' not sure when to use, or if I should change the PERMANENT_SESSION_LIFETIME = 600 seconds
app.config['JSON_SORT_KEYS'] = False


###home page
### GOAL: Check's for user access token, if exists, goes to home page else re-directs to login page
@app.route('/')
def index():
    if session.get("access_token") is None:  
        conn = sqlite3.connect("playlists_created_db.db")
        c = conn.cursor()

        sql_query = c.execute("SELECT *  FROM playlists_created") ###SQL Query
        playlists_created = sum([k[0] for k in sql_query])

        sql_query = c.execute("SELECT *  FROM playlists_created") ###SQL Query
        songs_added = sum([x[1] for x in sql_query])

        return render_template("login.html",playlists_created = playlists_created, songs_added = songs_added)  ###ACCESS TOKEN NOT FOUND: LOGIN PAGE

    else:
        conn = sqlite3.connect("playlists_created_db.db")
        c = conn.cursor()
        
        sql_query = c.execute("SELECT *  FROM playlists_created") ###SQL Query
        playlists_created = sum([k[0] for k in sql_query])
        
        sql_query = c.execute("SELECT *  FROM playlists_created") ###SQL Query
        songs_added = sum([x[1] for x in sql_query])
        
        return render_template("index.html",playlists_created = playlists_created, songs_added = songs_added)  ### ACCESS TOKEN FOUND
    

###################### --------------------USER AUTHORIZATION --------------------##############################
cid ="b67120ec7a07409fad337b38ff8c996d" 
#r_uri = "http://localhost:5000/callback"
r_uri = "https://spotifythebestof.herokuapp.com/callback"
scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-top-read "
scope = scope.replace(" ", "%20")

# code_verifier = None
# code_challenge= None
# code_verifier,code_challenge = create_code_verifier_challenge(code_verifier=code_verifier, code_challenge=code_challenge)
# session['code_verifier'] = code_verifier
# session['code_challenge'] = code_challenge

### FIX ISSUE: Want to be using the functions form generate_codes.py to create these but can't get them to stop changing
code_verifier ="ECEtZV02HFwfo2UbYDmvtV98AxicCSlKSQtbFww8PSWVNnAYmH"   
code_challenge = "g40RsQQwAVI9_biHTQxb5t-2CKNFvMQFN1gmUjKOpWE"


### Get's user authorization code
@app.route('/auth', methods=['GET'])
def auth():
    # code_verifier,code_challenge = create_code_verifier_challenge()
    # session['code_verifier'] = code_verifier
    # session['code_challenge'] = code_challenge
    # code_verifier = session.get('code_verifier')
    # code_challenge = session.get('code_challenge')
    return redirect('https://accounts.spotify.com/authorize' + '?response_type=code' + '&client_id=' + cid + '&redirect_uri=' + r_uri + '&scope=' + scope + '&code_challenge='+str(code_challenge) + '&code_challenge_method=S256')

###SPOTIFY API redirects to this page and provides the access_token in the HTML response. 
#### PARSE RESPONSE DATA FROM THE URL and redirect to index page
@app.route('/callback', methods=['GET','POST'])
def callback():
    code = request.args.get('code')  ##retrieve authorization code -> exchange for access_token -> sp.spotify(auth=acces_tocken) 
    if code is not None:
        # code_verifier = session.get('code_verifier')
        # code_challenge = session.get('code_challenge')
        #get access token using REST API
        url = "https://accounts.spotify.com/api/token"
        grant_type = "authorization_code"
        parameters = {'client_id':cid,'grant_type':grant_type, 'code':code, "redirect_uri":r_uri,'code_verifier':code_verifier}
        response = requests.post(url =url,data=parameters)  ### had to import requests
        response_data = response.json()
        access_token = response_data['access_token']
        session['access_token'] = access_token 
        return redirect(url_for('index'))
        
    else: 
        error = request.args.get('error')
        return "Please login again"

###################### --------------------END USER AUTHORIZATION --------------------##############################
#########################################################################################################################3


@app.route('/', methods=['POST','GET']) ### this line takes in the put from the search field on home page and POSTS to
def index_post():
    user_search = str(request.form['user_search'])
    
    ### assumes the only error is expired token, so just login again
    ### AUTHENTICATING SERVER/ EXPIRING TOKEN: https://github.com/felix-hilden/tekore/blob/master/docs/src/examples/auth_server.rst
    try: 
        playlists = keyWordPlaylist(user_search, access_token=session.get("access_token")) 
    except:
        return render_template('login.html') 

    playlists_dict = { k[0]: k[1:] for k in playlists } ### convert to a dict to pass to template. in HTML file, loop through dict to make HTML table
                                                        ### {uri:name, numSongs} to avoid same name removal during dict creation. Lazy workaround b/c rest of code
    
    total_tracks = sum(x[2] for x in playlists)
    totalPlaylists = len(playlists)
    
    session['playlists'] = playlists
    session['query'] = user_search
    
    return render_template('Playlists.html', playlists_dict=playlists_dict,usersearch = user_search, totalPlaylists = totalPlaylists,total_tracks=total_tracks)
    
@app.route('/collectTracks', methods=['POST'])
def collectTracks():     
    numOfPlaylists = float(request.form.get('numOfPlaylists'))
    
    playlists = session.get('playlists')
    
    ## takes user input for length of search
    totalPlaylists = len(playlists)
    playlists_to_search = round(totalPlaylists*numOfPlaylists)
    playlists = playlists[:playlists_to_search]

    ## API REQUESTS  
    all_tracks = get_tracks_from_all_playlists(playlists, access_token=session.get("access_token"))
    uniqueTracks = get_unique_tracks_from_all_tracks(all_tracks)
    uniqueTracks = uniqueTracks[:250]
    uniqueTracks_dict = { k[0]:k[1] for k in uniqueTracks}

    session['uniqueTracks'] = uniqueTracks
    
    user_search = session.get('query')
    
    return render_template('Tracks.html', uniqueTracks_dict=uniqueTracks_dict, user_search = user_search)


@app.route('/savePlaylist', methods =['POST'])
def savePlaylist():
    playlistName = "Best Of: " + str(session.get('query'))
    numOfTracks = int(request.form.get('numOfTracks'))
    
    uniqueTracks = session.get('uniqueTracks')
    uniqueTracks = uniqueTracks[:numOfTracks]    
    access_token = session.get('access_token')
    
    ### API request to get user ID
    response = requests.get(url="https://api.spotify.com/v1/me", headers={'Authorization': f'Bearer {access_token}'})
    response_data = response.json()
    id = response_data["id"]
    
    createPlaylist_get_Id = create_playlist_add_tracks( playlistName=playlistName,uniqueTracks=uniqueTracks, access_token= access_token, numofSongs=numOfTracks,id=id)
    
    ##SQL
    conn = sqlite3.connect("playlists_created_db.db")
    c = conn.cursor()
    create_tables()

    playlists_created(1,numOfTracks)
    return render_template('Playlist_saved.html', user_search =str(session.get('query')), playlistURI = createPlaylist_get_Id )
####-------------------------------------------------------------

@app.route('/about')
def about():
    return render_template('About.html')

