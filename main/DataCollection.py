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

####-------------------------------------------------------------

cid ="b67120ec7a07409fad337b38ff8c996d" 
secret = "69b703aa3746448ab5d3714fdc2c4994"
r_uri =  "http://localhost:8888/callback/"
username = "12181305850"

###---------------------------------------------------------------


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid,
                                                client_secret=secret,
                                                redirect_uri=r_uri,
                                                scope="user-library-read playlist-read-private playlist-modify-public user-top-read"))
###---------------------------------------------------------------------
### this pulls out relevant information about the track from a playlist and stores in a matrix
### input: 1 playlist

# sourcePlaylist = sp.playlist_items("6nU0t33tQA2i0qTI5HiyRV", fields= 'items.track')["items"]

# playlistTracks = [[0]*4 for i in range(len(sourcePlaylist))]

# for i in range(0,len(sourcePlaylist)):
#     playlistTracks[i][0] = sourcePlaylist[i]["track"]["name"]
#     playlistTracks[i][1] = sourcePlaylist[i]["track"]["artists"][0]["name"]
#     playlistTracks[i][2] = sourcePlaylist[i]["track"]["id"]
#     playlistTracks[i][3] = sourcePlaylist[i]["track"]["uri"]




###--------------------------------------------------------------
### user's most listened to tracks

# sourceMostListened = sp.current_user_top_tracks(time_range = ['long_term'], limit=50)["items"]

# mostListened = [[0]*4 for i in range(len(sourceTopTracks))]

# for i in range(0,len(sourceTopTracks)):
#     mostListened[i][0] = sourceMostListened[i]["name"]
#     mostListened[i][1] = sourceMostListened[i]["artists"][0]["name"]
#     mostListened[i][2] = sourceMostListened[i]["id"]
#     mostListened[i][3] = sourceMostListened[i]["uri"]




### add songs to "GOOD SONGS" playlist
### add songs to "BAD SONGS" playlist
    
#sp.user_playlist_add_tracks(username,"0mUxw2FqoIYgvTZRyZfP3F",[songs[i]["track"]["id"]])

###-------------------------------------------------------------------
### Find popular playlists based on query (name)
### then find all songs in playlists and count frequency of each song

### try to replicate keyWordPlaylists using "next". Right now, there is a limit of 50 results, next offsets by 50 every time


def keyWordPlaylist(query:str()):
    
    
    sourceFindPlaylists = sp.search(q=query,type="playlist", limit=50)

    total_playlists = len(sourceFindPlaylists["playlists"]["items"]) ### total playlists found from query

    playlists = [] ### initialize empty playlist list
    counter = 0 ### counter to loop through each set of 50 playlists
    counter_offset = 0 ### used to limit the number of playlists to include in search. Done via loop using "next" token


    while sourceFindPlaylists["playlists"]["next"] :
        
        playlistName= sourceFindPlaylists["playlists"]["items"][counter]["name"]
        
        playlistId= sourceFindPlaylists["playlists"]["items"][counter]["id"]
        
        playlistTrackCount =sourceFindPlaylists["playlists"]["items"][counter]["tracks"]["total"]
        
        playlists.append([playlistName, playlistId, playlistTrackCount])
        
        counter+=1            
        if counter == 50: counter = 0
        
        counter_offset +=1
        if counter_offset == 200:
            break

    return playlists

playlists = keyWordPlaylist("hip hop kanye")  ### returns a list of playlist: name/id/trackCount



## find songs from playlists (playlist_id) and then count frequency



""" allTracks = []

### this for loop iterates via each playlist to append tracks to allTracks
for i in range(0,len(playlists)):
    
    ### iterate playlist (id)
    
    playlist_temp = playlists[i][1]
    playlistTrackCount = playlists[i][2]    
    
    ### append all tracks to playlist. then apply element:counter for a freq ofunique variable
    
   
    playlistTracks = sp.playlist_tracks(playlist_id=playlist_temp, limit=100)
    
    tracks_temp = []
    counter = 0
    
    
    while playlistTracks["next"] == None:
        trackName_temp = playlistTracks["items"][counter]["track"]["name"]
        trackId_temp = playlistTracks["items"][counter]["track"]["id"]
        counter +=1
        
    counter = 0
        
    while playlistTracks["next"]: 
        
        for i in range(0,playlistTrackCount):
            trackName = playlistTracks["items"][i]["track"]["name"]
            trackId = playlistTracks["items"][i]["track"]["id"]
            allTracks.append([trackName, trackId])
    
        TopTracks = Counter(allTracks)
     """


# def getPlaylistTracks(topPlaylists:list)
    # topTracks =[]
    # for i in range(0,5):
    #     sourceTopTracks = sp.playlist_tracks(playlist_id=topPlaylists[0][1], limit=10)["items"] ## limit is the number of songs per playlist
    #     for j in range(0,len(sourceTopTracks)):
    #         trackName = sourceTopTracks[j]["track"]["name"]
    #         trackId = sourceTopTracks[j]["track"]["id"]
    #         topTracks.append([trackName, trackId])
    




# sourceTopTracks = sp.playlist_tracks(playlist_id="5Opo01VU7zfMlk6Yd8vMIJ", limit=100)

# counter = 0
# allTracks = [] ### append all tracks to playlist. then apply element:counter for a freq ofunique variable
# global TopTracks

# while sourceTopTracks["next"]:
    
#     playlistTrackCount = playlists[counter][2]
    
#     for i in range(0,playlistTrackCount):
#         trackName = sourceTopTracks["items"][i]["track"]["name"]
#         trackId = sourceTopTracks["items"][i]["track"]["id"]
#         allTracks.append([trackName, trackId])
    
#     TopTracks = Counter(allTracks)
    
    
    













































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
#         playlistId= sourceFindPlaylists["playlists"]["items"][0]["id"]
#         topPlaylists.append([playlistName, playlistId])
    
#     return topPlaylists

# keyWordPlaylists("work out")


















