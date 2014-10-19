from flask import Flask, render_template, request
from mopidy import *

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def hello():
    if request.method == 'POST':
        if request.form.has_key('new_playlist'):
            player = Mopidy()
            player.play_new_playlist()

    return render_template('server.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
