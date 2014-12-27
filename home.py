import subprocess
import time
import sys
from mopidy import Mopidy
from logger import Logger

print 'WTF'
# sys.stdout = Logger()
# Ten Minutes
OFF_COUNTER = 60

not_home_counter = 0
home_counter = 0

startup = True

update_playlist = True

print "Downloading Playlists"
player = Mopidy()

# Once above is done lets make it check every like... 5 seconds?
# We will need a better way to scan the network.
# Something quick that looks for the mac address of the phone

while True:
    print 'Scanning...'
    found = False
    
    arpcmd="arp -a -n"
    arp = subprocess.check_output(arpcmd, shell=True)
    arp_num = arp.find('f8:a9:d0:63:16:d9')

    print arp_num

    if arp_num > 0:
        ip_found = False
        ip = ''
        ip_record = False

        while not ip_found:
            if arp[arp_num] == ')':
                ip_record = True
            elif arp[arp_num] == '(':
                ip_found = True
            elif ip_record:
                ip = arp[arp_num] + ip
            elif arp_num < 0:
                ip = ''
                ip_found = True

            arp_num -= 1

        print 'IP: %s' % ip
        batcmd = "nmap -sn %s" % ip
        nmap = subprocess.check_output(batcmd, shell=True)

        if nmap.find('host up') >= 0:
            found = True
            print "Found"
            not_home_counter = 0

            if home_counter < 0:
                home_counter = 0

            elif home_counter == 0:
                state = player.get_state()
                if state == 'paused' or state == 'stopped' and not startup:
                    subprocess.check_output('wemo switch "light" on', shell=True)
                    player.play_new_playlist()
                    subprocess.check_output('wemo switch "main" on', shell=True)

            home_counter += 1

    if not found:
        print "NOT Found"

        if home_counter > 0 and not_home_counter == 0:
            home_counter = OFF_COUNTER
        elif home_counter > 0 and not_home_counter > 0:
            home_counter -= 1

        not_home_counter += 1

        # 10 Mins - Want to be able to walk to bodega and stuff without turning off
        if not_home_counter == OFF_COUNTER:
            player.pause()
            subprocess.check_output('wemo switch "main" off', shell=True)
            subprocess.check_output('wemo switch "light" off', shell=True)

    # Update playlists at 5:30AM Every Night
    #now = time.gmtime()
    #if update_playlist and now.tm_hour == 10 and now.tm_min == 30:
    #    player.save_playlists()
    #    update_playlist = False 
    #elif now.tm_hour == 5 and now.tm_min == 0:
    #    update_playlist = True

    print home_counter
    print not_home_counter
    startup = False
    time.sleep(10)
