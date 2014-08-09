import RPi.GPIO as GPIO
from mopidy import Mopidy

BUTTON_PIN = 25
LIGHT_PIN = 22
#NEW_BUTTON_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
# GPIO.setup(NEW_BUTTON_PIN, GPIO.IN)

print('Started...')
print('Getting Playlists...')
player = Mopidy()
print('Started')

player.play_new_playlist()

prev_input = 1
while True:
    input = GPIO.input(BUTTON_PIN)

    if prev_input != input and not input:
        print("Button Pushed DOWN")
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
	
        state = get_state()
        print state
        if state == 'paused' or state == 'stopped':
            player.resume()
        else:
            player.pause()
            
    elif prev_input != input and input:
        print("Button Released")
        GPIO.output(LIGHT_PIN, GPIO.LOW)

    prev_input = input
    time.sleep(0.05)
