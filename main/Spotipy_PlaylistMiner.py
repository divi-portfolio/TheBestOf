"""
Created on Tue Sep 29 19:30:57 2020
@author: divim
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
###-------------------------------------------------------------------
### Find popular playlists based on query (name)
### then find all songs in playlists and count frequency of each song

def create_sp(access_token:str):
    sp = spotipy.Spotify(auth=access_token)
    return sp

def keyWordPlaylist(query:str, access_token): 
    sp = create_sp(access_token)
    sourceFindPlaylists = sp.search(q=query,type="playlist", limit=50)### 50 is api limit

    total_playlists = sourceFindPlaylists["playlists"]["total"] ### total playlists found from query


    if total_playlists >=49: ### only 49, not 50 (api limit) b/c some queries only returned 49 but next was true, so the code would break searching out of limit
        total_playlists = 49 

    global playlists
    playlists = [] ### initialize empty playlist list

    
    for i in range(0,total_playlists):
        playlistName= sourceFindPlaylists["playlists"]["items"][i]["name"]
        playlistUri= sourceFindPlaylists["playlists"]["items"][i]["uri"]
        playlistTrackCount =sourceFindPlaylists["playlists"]["items"][i]["tracks"]["total"]
        playlists.append([playlistUri, playlistName,  playlistTrackCount])
        
   
    while sourceFindPlaylists["playlists"]["next"]:
        
        if len(playlists) >= 50: ### that number + 49 playlists to find total
            break
        
        sourceFindPlaylists = sp.next(sourceFindPlaylists["playlists"])
        playlistCount = len(sourceFindPlaylists["playlists"]["items"])
        
        for i in range(0,playlistCount):
            
            playlistName= sourceFindPlaylists["playlists"]["items"][i]["name"]
            
            playlistUri= sourceFindPlaylists["playlists"]["items"][i]["uri"]
            
            playlistTrackCount =sourceFindPlaylists["playlists"]["items"][i]["tracks"]["total"]
            
            playlists.append([playlistUri, playlistName,  playlistTrackCount])

    
    return playlists



def get_playlist_tracks(playlist_id:str, access_token):
    sp = create_sp(access_token)
    global tracks
    tracks=[]
    ### first api return 
    results = sp.playlist_tracks(playlist_id = playlist_id, limit=100) 
    playlistTrackCount = results["total"] 
      
    if playlistTrackCount > 100:  ### to ensure that iteration doesn't go out of range
        playlistTrackCount = 100
       
        ### for the first 
    for i in range(0,playlistTrackCount):
        
        try:
            trackName = results["items"][i]["track"]["name"]
            trackId = results["items"][i]["track"]["uri"]
            tracks.append([trackId,trackName])
        
        except:
            pass
            
        ### loop through remaining playlists
    while results["next"]:
        
        results = sp.next(results)
        playlistTrackCount = len(results["items"])
        
        for i in range(0,playlistTrackCount):
            
            try:
                
                trackName = results["items"][i]["track"]["name"]
                trackId = results["items"][i]["track"]["uri"]
                tracks.append([trackId,trackName])
        
            except:
                pass
            
    return tracks
#############################

def get_tracks_from_all_playlists(playlists:list,access_token):
    sp = create_sp(access_token)
    global all_tracks
    all_tracks = []
    for each in playlists:
        all_tracks = all_tracks + get_playlist_tracks(each[0],access_token) ### call function to get all track from playlist and append to tracks. This runs through all playlists in playlists
    return all_tracks

    
def get_unique_tracks_from_all_tracks(all_tracks:list):
    global uniqueTracks
    uniqueTracks =[]
    
    
    uniqueTracks = Counter( tuple(item) for item in all_tracks).most_common()  ### convert a list of list into list of tuples
    uniqueTracks = list(zip(*uniqueTracks))[0] ## remove the freq. count to only keep a list of tuples(name, id)
    uniqueTracks = [ list(x) for x in uniqueTracks] ### convert list of tuples to list of lists 
    
    return uniqueTracks ### returns unique tracks (TUPLE) URI and Name from all the playlists in descending popularity (removed freq count)

###############################

def create_playlist_add_tracks(playlistName:str, uniqueTracks, access_token, id,numofSongs=100): 
    sp = create_sp(access_token)
    sp.user_playlist_create(user =id, name= playlistName)
    
    
    userPlaylists_temp = sp.current_user_playlists()["items"] ### get list of all user playlists. Find the playlist id of the playlist we just created
        
    for each in userPlaylists_temp:
        if each["name"] == playlistName:
            playlistId_temp = each["uri"]
    
    uniqueTracks_uri= [x[0] for x in uniqueTracks]
    

    if numofSongs < 100 :
        sp.playlist_add_items(playlist_id = playlistId_temp, items = uniqueTracks_uri[0:numofSongs] )

    elif numofSongs == 99:
        sp.playlist_add_items(playlist_id = playlistId_temp, items = uniqueTracks_uri[0:100] )
    else:
        s = 25
        for i in range(0,len(uniqueTracks_uri),s):
            if (i+s) > numofSongs:
                break
            else:
                sp.playlist_add_items(playlist_id = playlistId_temp, items = uniqueTracks_uri[i:i+s] )
        
    return playlistId_temp
            

       

# ########################## 

# playlists = keyWordPlaylist("J Cole")  ### returns a list of playlist: name/id/trackCount

# get_tracks_from_all_playlists(playlists) 

# get_unique_tracks_from_all_tracks(all_tracks)

# create_playlist_add_tracks(playlistName="TESTERabc", uniqueTracks = uniqueTracks)



### types of possible projects:


### 1. TOP SONGS Find all popular playlists based on keywords. Then filter for most frequent tracks
### 2. Filter based on audio features, artists, genre
### 3. Recommend songs based on top listened to by user
### 4. Implement machine learning to find songs based on audio features

    

### playlist_items() gives these info per track and more: album
# artists
# available_markets
# disc_number
# duration_ms
# episode
# explicit
# external_ids
# external_urls
# href
# id
# is_local
# name
# popularity
# preview_url
# track
# track_number
# type
# uri




































