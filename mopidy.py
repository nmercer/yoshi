import requests
import json
import random

MOPIDY_URL = 'http://localhost:6680/mopidy/rpc'

class Mopidy(object):

    def __init__(self):
        self.playlists = self.get_playlists()
        self.playlist = None
        self.volume = 100

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

    def shuffle(self, shuffle):
        params = {'shuffle':shuffle}
        self.send('core.tracklist.set_shuffle', params=params)
