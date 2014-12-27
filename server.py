from flask import Flask, jsonify, render_template, request
from mopidy import *
from flask_bootstrap import Bootstrap
import subprocess

#app = Flask(__name__)

def create_app(configfile=None):
    app = Flask(__name__)
    Bootstrap(app)

    @app.route("/volume", methods = ['GET'])
    def volume():
        player = Mopidy()
        print(int(request.args.get('volume')))
        player.set_volume(int(request.args.get('volume')))
        return jsonify({'success':True})

    @app.route("/register", methods = ['GET'])
    def register():
        print request.remote_addr
        return jsonify({'success':True})

    @app.route("/random", methods = ['GET'])
    def random():
        player = Mopidy()
        player.play_new_playlist()
        return jsonify({'success':True})

    @app.route("/lights", methods = ['GET'])
    def lights():
        subprocess.check_output('wemo switch "main" on', shell=True)
        subprocess.check_output('wemo switch "light" on', shell=True)

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

            elif request.form.has_key('switch_one_on'):
                subprocess.check_output('wemo switch "main" on', shell=True)
            elif request.form.has_key('switch_one_off'):
                subprocess.check_output('wemo switch "main" off', shell=True)

            elif request.form.has_key('switch_two_on'):
                subprocess.check_output('wemo switch "light" on', shell=True)
            elif request.form.has_key('switch_two_off'):
                subprocess.check_output('wemo switch "light" off', shell=True)
            elif request.form.has_key('goodnight'):
                subprocess.check_output('wemo switch "main" off', shell=True)
                subprocess.check_output('wemo switch "light" off', shell=True)
                player = Mopidy()
                player.pause()
        return render_template('server.html')

    return app

if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port=3000, debug=True)
