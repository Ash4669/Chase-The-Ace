from flask import Flask, render_template
from pusher import pusher

app = Flask(__name__)

@app.route('/')
def signInPage():
    return render_template('sign-in-page.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
