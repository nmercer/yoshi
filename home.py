import subprocess
import time
from mopidy import Mopidy

# Ten Minutes
OFF_COUNTER = 60

not_home_counter = 0
home_counter = 0

print "Downloading Playlists"
player = Mopidy()

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

        if home_counter < 0:
            home_counter = 0

        elif home_counter == 0:
            state = player.get_state()
            if state == 'paused' or state == 'stopped':
                player.play_new_playlist()
                subprocess.check_output('wemo switch "main" on', shell=True)

        home_counter += 1

    else:
        print "NOT Found"

        if home_counter > 0:
            home_counter = OFF_COUNTER - 1
        elif home_counter < 0:
            home_counter += 1

        not_home_counter += 1

        # 10 Mins - Want to be able to walk to bodega and stuff without turning off
        if not_home_counter == OFF_COUNTER:
            player.pause()
            subprocess.check_output('wemo switch "main" off', shell=True)

    time.sleep(10)
