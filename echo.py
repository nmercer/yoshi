from amazon_echo import Echo
import sched, time
import subprocess
from mopidy import *

scheduler = sched.scheduler(time.time, time.sleep)
echo = Echo('nm3rc3r@gmail.com', 'RedMetal8*')
player = Mopidy()

# Runs Every 5 Seconds and prints out what you last said
def main(scheduler):
    todo = echo.get_latest_todo()
    print "Todo: %s" % todo

    if todo:
        lights = False
        if todo.find("lights") > -1 or todo.find("light") > -1:
            lights = True
        
        off = False
        if todo.find("off") > -1 or todo.find("out") > -1:
            off = True

        next_song = False
        if todo.find("next") > -1 or todo.find("skip") > -1:
            next_song = True

        play_song = False
        #if todo.find("play") > -1:
        #    play_song = True

        pause_song = False
        if todo.find("pause") > -1 or todo.find("stop") > -1:
            pause_song = True

        random_playlist = False
        if todo.find("random") > -1 or todo.find("shuffle") > -1 or todo.find("play") > -1:
            random_playlist = True

        if lights and not off:
            subprocess.check_output('wemo switch "light" on', shell=True)
            subprocess.check_output('wemo switch "main" on', shell=True)
        elif lights and off:
            subprocess.check_output('wemo switch "main" off', shell=True)
            subprocess.check_output('wemo switch "light" off', shell=True)        
        
        if next_song:
            player.next_song()
        if play_song:
            player.play()
        if pause_song:
            player.pause()
        if random_playlist:
            player.play_new_playlist()

    scheduler.enter(5, 1, main, (scheduler,))

scheduler.enter(0, 1, main, (scheduler,))
scheduler.run()
