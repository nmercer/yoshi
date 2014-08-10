import subprocess
import time
from mopidy import Mopidy

not_home_counter = 0
print "Downloading Playlists"
player = Mopidy()
home_counter = 0

while True:
	print "Checking If Home"

	batcmd="for X in $(hostname -I) ; do nmap -sP ${X}/24 ; done"
	nmap = subprocess.check_output(batcmd, shell=True)

	if nmap.find('192.168.1.4') >= 0:
		print "Found" 
		not_home_counter = 0
		if home_counter == 0:
            		state = player.get_state()
            		if state == 'paused' or state == 'stopped':			
				player.play_new_playlist()
		home_counter += 1

        else:
		print "NOT Found"
		home_counter = 0
		not_home_counter += 1
		if not_home_counter == 5:
			player.pause()

	time.sleep(60)
