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

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 19:30:57 2020

@author: divim
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import spotipy.util as util

from collections import Counter

##### MANUAL DEBUGGING FOR MY PERSONAL ACCOUNT-------------------------------------------------------------

# cid ="b67120ec7a07409fad337b38ff8c996d" 
# secret = "4076d89b161441b5ae99ac66497f35be"
# r_uri =  "http://localhost:8888/callback/"
# username = "12181305850"

# ###---------------------------------------------------------------


# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid,
#                                                 client_secret=secret,
#                                                 redirect_uri=r_uri,
#                                                 scope="user-library-read playlist-read-private playlist-modify-public user-top-read playlist-modify-public"))
###---------------------------------------------------------------------




###-------------------------------------------------------------------
### Find popular playlists based on query (name)
### then find all songs in playlists and count frequency of each song

### FUNCTIONALITY TO ADD:
    ### when using as a website: create query fields for artist, genre, OR, NOT. RESULT: WONT WORK B/C searching playlists not tracks 
    ### Number of songs to include in playlist
    ###     
    ###Make playlists editable. currently unable to remove songs 

def create_sp(access_token:str):
    sp = spotipy.Spotify(auth=access_token)
    return sp

def keyWordPlaylist(query:str, access_token): ### this works great except if the less than 50 playlists found
    sp = create_sp(access_token)
    sourceFindPlaylists = sp.search(q=query,type="playlist", limit=50)### 50 is api limit

    total_playlists = sourceFindPlaylists["playlists"]["total"] ### total playlists found from query


    if total_playlists >=49:
        total_playlists = 49 

    global playlists
    playlists = [] ### initialize empty playlist list

    
    for i in range(0,total_playlists):
        playlistName= sourceFindPlaylists["playlists"]["items"][i]["name"]
        playlistUri= sourceFindPlaylists["playlists"]["items"][i]["uri"]
        playlistTrackCount =sourceFindPlaylists["playlists"]["items"][i]["tracks"]["total"]
        playlists.append([playlistUri, playlistName,  playlistTrackCount])
        
   
    while sourceFindPlaylists["playlists"]["next"]:
        
        if len(playlists) >= 50: ### change to 1000 after debugging
            break
        
        sourceFindPlaylists = sp.next(sourceFindPlaylists["playlists"])
        playlistCount = len(sourceFindPlaylists["playlists"]["items"])
        
        for i in range(0,playlistCount):
            
            playlistName= sourceFindPlaylists["playlists"]["items"][i]["name"]
            
            playlistUri= sourceFindPlaylists["playlists"]["items"][i]["uri"]
            
            playlistTrackCount =sourceFindPlaylists["playlists"]["items"][i]["tracks"]["total"]
            
            playlists.append([playlistUri, playlistName,  playlistTrackCount])
            
           
        # num_of_playlists +=50
    
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

#playlists = keyWordPlaylist("Jay Sean")  ### returns a list of playlist: name/id/trackCount

# get_tracks_from_all_playlists(playlists) 

# get_unique_tracks_from_all_tracks(all_tracks)

# create_playlist_add_tracks(playlistName="TESTERabc", uniqueTracks = uniqueTracks)




# c.close()
# conn.close()











































#### ARCHIVE
#########################################################################
#########################################################################


### find popular playlists. Output: topPlayLists has playlist Name and ID

# def keyWordPlaylists(query:str):
#     query.replace(" ","%20")
#     sourceFindPlaylists = sp.search(q=query,type="playlist", limit=50)
#     global topPlaylists
#     topPlaylists = []
    
#     for i in range(0,limit):
        
#         playlistName= sourceFindPlaylists["playlists"]["items"][i]["name"]
#         playlistId= sourceFindPlaylists["playlists"]["items"][0]["uri"]
#         topPlaylists.append([playlistName, playlistId])
    
#     return topPlaylists

# keyWordPlaylists("work out")



## find songs from playlists (playlist_id) and then count frequency



# allTracks = []



# ### this for loop iterates via each playlist to append tracks to allTracks

# for i in range(0,len(playlists))
    
#     ### iterate playlist (id)
    
#     playlist_temp = playlists[i][1]
#     playlistTrackCount = playlists[i][2]    
    
#     ### append all tracks to playlist. then apply element:counter for a freq ofunique variable
    
   
#     playlistTracks = sp.playlist_tracks(playlist_id=playlist_temp, limit=100)
    
#     tracks_temp = []
#     counter = 0
    
    
#     while playlistTracks["next"] = None:
#         trackName_temp = playlistTracks["items"][counter]["track"]["name"]
#         trackId_temp = playlistTracks["items"][counter]["track"]["uri"]
#         counter +=1
        
#     counter = 0
        
#     while playlistTracks["next"]: 
        
#         for i in range(0,playlistTrackCount):
#             trackName = playlistTracks["items"][i]["track"]["name"]
#             trackId = playlistTracks["items"][i]["track"]["uri"]
#             allTracks.append([trackName, trackId])
    
#         TopTracks = Counter(allTracks)
    


# def getPlaylistTracks(topPlaylists:list)
    # topTracks =[]
    # for i in range(0,5):
    #     sourceTopTracks = sp.playlist_tracks(playlist_id=topPlaylists[0][1], limit=10)["items"] ## limit is the number of songs per playlist
    #     for j in range(0,len(sourceTopTracks)):
    #         trackName = sourceTopTracks[j]["track"]["name"]
    #         trackId = sourceTopTracks[j]["track"]["uri"]
    #         topTracks.append([trackName, trackId])
    




# sourceTopTracks = sp.playlist_tracks(playlist_id="5Opo01VU7zfMlk6Yd8vMIJ", limit=100)

# counter = 0
# allTracks = [] ### append all tracks to playlist. then apply element:counter for a freq ofunique variable
# global TopTracks

# while sourceTopTracks["next"]:
    
#     playlistTrackCount = playlists[counter][2]
    
#     for i in range(0,playlistTrackCount):
#         trackName = sourceTopTracks["items"][i]["track"]["name"]
#         trackId = sourceTopTracks["items"][i]["track"]["uri"]
#         allTracks.append([trackName, trackId])
    
#     TopTracks = Counter(allTracks)







# ########
# def keyWordPlaylist(query:str()): ### this works great except if the less than 50 playlists found
#     # query = query.replace(" ", "%20")
    
#     sourceFindPlaylists = sp.search(q=query,type="playlist", limit=50)### 50 is api limit

#     total_playlists = len(sourceFindPlaylists["playlists"]["items"]) ### total playlists found from query

    
#     playlists = [] ### initialize empty playlist list
#     counter = 0 ### counter to loop through each set of 50 playlists
#     num_of_playlists = 0 ### used to limit the number of playlists to include in search. Done via loop using "next" token


#     while sourceFindPlaylists["playlists"]["next"]:
        
#         playlistName= sourceFindPlaylists["playlists"]["items"][counter]["name"]
        
#         playlistId= sourceFindPlaylists["playlists"]["items"][counter]["uri"]
        
#         playlistTrackCount =sourceFindPlaylists["playlists"]["items"][counter]["tracks"]["total"]
        
#         playlists.append([playlistName, playlistId, playlistTrackCount])
        
#         counter+=1            
#         if counter == 50: counter = 0
        
#         num_of_playlists +=1
#         if num_of_playlists == 1000:
#             break

#     return playlists
