#!/bin/sh

sleep 90
# Remove the stupid cache thats always fucked
cd /
cd home/pi/.wemo
rm cache

# Start the scripts
cd /
cd home/pi/button-play 
sudo python controller.py &
sudo python home.py &

cd /
