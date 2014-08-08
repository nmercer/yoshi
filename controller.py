import requests
import json
import RPi.GPIO as GPIO
import time

BUTTON_PIN = 25
LIGHT_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.setup(LIGHT_PIN, GPIO.OUT)

MOPIDY_URL = 'http://localhost:6680/mopidy/rpc'

def send(method):
    data = json.dumps({"jsonrpc": "2.0", "id": 1, "method": str(method)})
    r = requests.post(MOPIDY_URL, data=data)
    return r.json()

def resume():
    send('core.playback.resume')

def pause():
    send('core.playback.pause')

def get_state():
    return send('core.playback.get_state')['result']

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
