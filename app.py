from flask import Flask, render_template
from pusher import pusher
import configparser

config = configparser.ConfigParser()
config.read("settings.conf")

app = Flask(__name__)

pusher = pusher_client = pusher.Pusher(
  app_id  = config.get('PUSHERDETAILS','app_id'),
  key     = config.get('PUSHERDETAILS','key'),
  secret  = config.get('PUSHERDETAILS','secret'),
  cluster = config.get('PUSHERDETAILS','cluster'),
  ssl     = bool(config.get('PUSHERDETAILS','ssl'))
)

@app.route('/')
def signInPage():
    pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
    return render_template('sign-in-page.html')

@app.route('/play')
def play():
    return render_template('play.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
