import requests
import json
import random
import sqlite3

MOPIDY_URL = 'http://localhost:6680/mopidy/rpc'

class Mopidy(object):

    def __init__(self, load_playlists=True):
        # Todo - Make this populate in the background
        self.check_database()
        
        if load_playlists:
            self.playlists = self.get_playlists()
            self.save_playlists()

        self.playlist = None
        self.volume = 100

    # Database Stuff
    def save_playlists(self):
        for playlist in self.playlists:
            if not self.db("SELECT * FROM playlists WHERE id='%s';" % playlist['uri'], row_exists=True):
                name = playlist['name'].replace("'", "")
                self.db("INSERT INTO playlists (name, id) VALUES('%s', '%s')" % (name, playlist['uri']))

    def db(self, query, row_exists=False):
        print query
        conn = sqlite3.connect('playlists.db')
        c = conn.cursor()
        c.execute(query)

        data = None
        if row_exists:
            data = c.fetchone()

        conn.commit()
        conn.close()

        return data
       
    def check_database(self):
        try:
            self.create_db()
        except:
            pass

    def create_db(self):
        self.db('''CREATE TABLE playlists (name, id);''')

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
