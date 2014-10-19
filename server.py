from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('server.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
