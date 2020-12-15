### IN MAIN __init__.py file 
# #### avoids import error b/c of directory path issues
# try:
#     from .database_spotipy import create_tables, data_entry_playlist, data_entry_tracks, data_entry_userSearch
# except ImportError:
#     from database_spotipy import create_tables, data_entry_playlist, data_entry_tracks, data_entry_userSearch


import sqlite3


conn = sqlite3.connect("data.db")
c = conn.cursor()

##delete existing table
c.execute("DROP TABLE IF EXISTS playlists_db")
c.execute("DROP TABLE IF EXISTS all_tracks_db")
c.execute("DROP TABLE IF EXISTS userSearch_db")

conn.commit()

conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

##  CREATE TABLES:  Playlists,  all_tracks
def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS playlists_db(URI TEXT, name TEXT, numofSongs INT)')
    c.execute('CREATE TABLE IF NOT EXISTS all_tracks_db(URI TEXT, name TEXT)')    
    c.execute('CREATE TABLE IF NOT EXISTS userSearch_db(userSearch TEXT)')    
    
def data_entry_playlist(playlists):
    
    for item in playlists:
        uri_  = item[0]
        name_ = item[1]
        numofSongs_  = item[2]
        
        c.execute("INSERT INTO playlists_db (URI, name, numofSongs) VALUES (? , ? , ?)",
                  (uri_, name_, numofSongs_))
    conn.commit()
    # c.close()
    # conn.close()

def data_entry_tracks(all_tracks):
    
    for item in all_tracks:
        uri_  = item[0]
        name_ = item[1]
        
        c.execute("INSERT INTO all_tracks_db(URI, name) VALUES (? , ?)",
                  (uri_, name_))
        
    conn.commit()

def data_entry_userSearch(userSearch):
    c.execute("INSERT INTO userSearch_db(userSearch) VALUES (?) ", 
                (userSearch,))
    conn.commit()

#c.close()  
#conn.close()

# create_tables()

# data_entry_playlist(playlists)

