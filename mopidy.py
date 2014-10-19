import requests
import json
import random
import sqlite3

MOPIDY_URL = 'http://localhost:6680/mopidy/rpc'

class Mopidy(object):

    def __init__(self, load_playlists=False):
        # Todo - Make this populate in the background
        self.check_database()        
        self.playlists = self.db_fetch('SELECT * FROM Playlists')

        print self.playlists
        print type(self.playlists)
        print dir(self.playlists)

        if load_playlists:
            self.save_playlists()

        self.playlist = None
        self.volume = 100

    # Database Stuff
    def save_playlists(self):
        playlists = self.get_playlists()

        for playlist in playlists:
            if not self.db_exists("SELECT * FROM Playlists WHERE id='%s';" % playlist['uri']):
                name = playlist['name'].replace("'", "")
                self.db_insert("INSERT INTO Playlists (Name, Id) VALUES('%s', '%s')" % (name, playlist['uri']))

    def db_fetch(self, query):
        conn = sqlite3.connect('playlists.db')
        c = conn.cursor()
        c.execute(query)

        data = c.fetchall()

        conn.commit()
        conn.close()

        return data


    def db_exists(self, query):
        conn = sqlite3.connect('playlists.db')
        c = conn.cursor()
        c.execute(query)

        data = c.fetchone()

        conn.commit()
        conn.close()

        if data:
            return True
        return data

    def db_insert(self, query):
        conn = sqlite3.connect('playlists.db')
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
       
    def check_database(self):
        try:
            self.db_insert('''CREATE TABLE Playlists (Name, Id);''')
        except:
            pass

    def send(self, method, params={}):
        data = json.dumps({"jsonrpc": "2.0", "id": 1, "method": str(method), "params":params})
        r = requests.post(MOPIDY_URL, data=data)
        return r.json()

    def resume(self):
        return self.send('core.playback.resume')

    def pause(self):
        return self.send('core.playback.pause')

    def get_state(self):
        return self.send('core.playback.get_state')['result']

    def get_playlists(self):
        return self.send('core.playlists.get_playlists')['result']

    # Todo - Store like last 10 playlist and don't grab any of those
    def get_random_playlist(self):
        return random.choice(self.playlists)['tracks']

    def clear_tracklist(self):
        return self.send('core.tracklist.clear')

    def add_to_tracklist(self, tracks):
        params = {'tracks':tracks}
        return self.send('core.tracklist.add', params=params)

    def get_tracklist(self):
        return self.send('core.tracklist.get_tracks')

    def get_track(self):
        return self.send('core.playback.get_current_tl_track')

    def get_track_name(self):
        data = self.get_track()
        return data['result']['track']['name'], data['result']['track']['artists'][0]['name']

    def play(self):
        return self.send('core.playback.play')

    def set_volume(self, volume):
        self.volume += volume
        if self.volume < 0:
            self.volume = 0
        elif self.volume > 100:
            self.volume = 100

        params = {'volume':self.volume}
        return self.send('core.playback.set_volume', params=params)

    def play_new_playlist(self):
        self.clear_tracklist()
        self.playlist = self.get_random_playlist()
        self.add_to_tracklist(self.playlist)
        self.play()

    def next_song(self):
        self.send('core.playback.next')

    def time_position(self):
        return self.send('core.playback.get_time_position')['result']

    # Todo - Not working
    def shuffle(self, shuffle):
        params = {'shuffle':shuffle}
        self.send('core.tracklist.set_shuffle', params=params)
