import requests
import json
import RPi.GPIO as GPIO
import time
import random

BUTTON_PIN = 25
LIGHT_PIN = 22
#NEW_BUTTON_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
#GPIO.setup(NEW_BUTTON_PIN, GPIO.IN)

MOPIDY_URL = 'http://localhost:6680/mopidy/rpc'

def send(method, params={}):
    data = json.dumps({"jsonrpc": "2.0", "id": 1, "method": str(method), "params":params})
    r = requests.post(MOPIDY_URL, data=data)
    return r.json()

def resume():
    return send('core.playback.resume')

def pause():
    return send('core.playback.pause')

def get_state():
    return send('core.playback.get_state')['result']

def get_playlists():
    return send('core.playlists.get_playlists')['result']

def get_random_playlist(playlists):
    return random.choice(playlists)['tracks']

def clear_tracklist():
    return send('core.tracklist.clear')

def add_to_tracklist(tracks):
    params = {'tracks':tracks}
    return send('core.tracklist.add', params=params)

def get_tracklist():
    return send('core.tracklist.get_tracks')

def get_track():
    return send('core.playback.get_current_tl_track')

def play():
    return send('core.playback.play')


print('Started...')
print('Getting Playlists...')

playlists = get_playlists()
playlist = get_random_playlist(playlists)

clear_tracklist()
add_to_tracklist(playlist)
play()

print('Ready...')

prev_input = 1
while True:
    input = GPIO.input(BUTTON_PIN)

    if prev_input != input and not input:
        print("Button Pushed DOWN")
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
	
        state = get_state()
        print state
        if state == 'paused' or state == 'stopped':
            resume()
        else:
            pause()
            
    elif prev_input != input and input:
        print("Button Released")
        GPIO.output(LIGHT_PIN, GPIO.LOW)

    prev_input = input
    time.sleep(0.05)
