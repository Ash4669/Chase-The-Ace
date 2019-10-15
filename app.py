from flask import Flask, render_template
from pusher import pusher

app = Flask(__name__)

pusher = pusher_client = pusher.Pusher(
  app_id='853461',
  key='7443318dffd154df2e7d',
  secret='ddfc4d7fd9521374a4c6',
  cluster='eu',
  ssl=True
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
