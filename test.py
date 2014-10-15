import subprocess
import sys
import espeak_py

print 'started'

#foo = subprocess.Popen([sys.executable, "home.py"])

#print foo
print 'ended' 

foo = espeak_py.init("/home/pi/button-play/")

speak_string = "Hello, World!"
options = {"speed":120}
file_name = "hello"

foo.say(speak_string, {"speed":120}, file_name)

#subprocess.check_output('wemo switch "wemo" on', shell=True)
