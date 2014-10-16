import subprocess
import time
from mopidy import Mopidy
from scapy.all import *

not_home_counter = 0
home_counter = 0

print "Downloading Playlists"
player = Mopidy()

# This could be made smarter by if it goes from Found to Not found
# if its not found first time, it sets home_counter to 5
# than for every new not found it reduces it by 1, untill it reaches 0
# than naturally once home is 0 it will start it back up
# if its not it will just keep skipping it again
# So you will have to be away for 5 loops before it would try to start it back up again
# This covers if you manually turn it off, it wont start up if you lose connection for a second to wifi

# Once above is done lets make it check every like... 5 seconds?
# We will need a better way to scan the network.
# Something quick that looks for the mac address of the phone

while True:
    print "Checking If Home"

    batcmd="nmap -sn 192.168.1.3"
    nmap = subprocess.check_output(batcmd, shell=True)

    if nmap.find('host up') >= 0:
        print "Found"
        not_home_counter = 0

        if home_counter == 0:
            state = player.get_state()
        if state == 'paused' or state == 'stopped':
            player.play_new_playlist()
            subprocess.check_output('wemo switch "main" on', shell=True)

        home_counter += 1

    else:
        print "NOT Found"

        if home_counter > 0:
            home_counter = -5
        elif home_counter < 0:
            home_counter += 1

        not_home_counter += 1

        if not_home_counter == 15:
            player.pause()
            subprocess.check_output('wemo switch "main" off', shell=True)

    print home_counter
    print not_home_counter

    time.sleep(60)
