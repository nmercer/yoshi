#!/bin/sh
# @reboot sh /home/pi/button-play/start.sh
sleep 90
# Remove the stupid cache thats always fucked
cd /
cd home/pi/.wemo
rm cache

cd /
cd root/.wemo
rm cache

# Start the scripts
# cd /
# cd home/pi/button-play 

# python controller.py &
# python home.py &
# python server.py &
