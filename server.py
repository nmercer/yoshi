from flask import Flask, render_template, request
from mopidy import *
import subprocess

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def hello():
    if request.method == 'POST':
        if request.form.has_key('new_playlist'):
            player = Mopidy()
            player.play_new_playlist()
        elif request.form.has_key('play'):
            player = Mopidy()
            player.play()
        elif request.form.has_key('pause'):
            player = Mopidy()
            player.pause()

        elif request.form.has_key('lights_on'):
            subprocess.check_output('wemo switch "main" on', shell=True)
        elif request.form.has_key('lights_off'):
            subprocess.check_output('wemo switch "main" off', shell=True)
            
    return render_template('server.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
