### IN MAIN __init__.py file 
# #### avoids import error b/c of directory path issues
# try:
#     from .database_spotipy import create_tables, data_entry_playlist, data_entry_tracks, data_entry_userSearch
# except ImportError:
#     from database_spotipy import create_tables, data_entry_playlist, data_entry_tracks, data_entry_userSearch


import sqlite3


conn = sqlite3.connect("playlists_created_db.db")
c = conn.cursor()

conn.commit()

conn = sqlite3.connect("playlists_created_db.db", check_same_thread=False)
c = conn.cursor()

##  CREATE TABLES:  Playlists,  all_tracks
def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS playlists_created(numofPlaylists INT, numofSongs INT)')
    
def playlists_created(numofPlaylists,numofSongs):
    
    c.execute("INSERT INTO playlists_created(numofPlaylists, numofSongs) VALUES (? , ?)",
                  ( numofPlaylists, numofSongs))
    conn.commit()
    c.close()
    conn.close()


#c.close()  
#conn.close()

# create_tables()

# data_entry_playlist(playlists)

