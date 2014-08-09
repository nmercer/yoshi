import time
import RPi.GPIO as GPIO
from mopidy import Mopidy

PLAY_PIN = 25
LIGHT_PIN = 22
NEXT_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(PLAY_PIN, GPIO.IN)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(NEXT_PIN, GPIO.IN)

print('Started...')
print('Getting Playlists...')
player = Mopidy()
print('Started')

player.play_new_playlist()
# print player.set_volume(100)

play_input_prev = 1
next_input_prev = 1
while True:
    #####################
    ## PLAY 
    #####################
    play_input = GPIO.input(PLAY_PIN)

    if play_input_prev != play_input and not play_input:
        print("Play Button Pressed")
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
	
        state = player.get_state()
        if state == 'paused' or state == 'stopped':
            player.resume()
        else:
            player.pause()
            
    elif play_input_prev != play_input and play_input:
        print("Play Button Released")
        GPIO.output(LIGHT_PIN, GPIO.LOW)

    play_input_prev = play_input

    #####################
    ## NEXT 
    #####################
    next_input = GPIO.input(NEXT_PIN)

    if next_input_prev != next_input and not next_input:
        print("Next Button Pressed")
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
    
        player.play_new_playlist()

            
    elif next_input_prev != next_input and next_input:
        print("Next Button Released")
        GPIO.output(LIGHT_PIN, GPIO.LOW)

    next_input_prev = next_input
    time.sleep(0.05)
