import collections
import copy
import datetime
import flask
import json
import threading

class Monitor(object):
  def __init__(self):
    self.lock = threading.Lock()

    self.tweet_count = 0
    self.recent_tweets = collections.deque()
    self.start_time = datetime.datetime.now()

    self.app = flask.Flask(__name__)

    @self.app.route("/")
    def index():
      return flask.redirect("/stats/recent")

    @self.app.route("/stats/recent")
    def recent():
      with self.lock:
        html = []
        html.append("<pre>")
        for tweet in self.recent_tweets:
          html.append(json.dumps(tweet, indent=4, sort_keys=True))
        html.append("</pre>")
        return "\n".join(html)

    @self.app.route("/stats/count")
    def count():
      with self.lock:
        return str(self.tweet_count)

    @self.app.route("/stats/uptime")
    def uptime():
      return str(datetime.datetime.now() - self.start_time)

    self.thread = threading.Thread(target=self.app.run, daemon=True)
    self.thread.start()

  def record_tweet(self, tweet):
    tweet = copy.copy(tweet)
    tweet["timestamp"] = str(tweet["timestamp"])
    print(json.dumps(tweet, indent=4, sort_keys=True))

    with self.lock:
      self.tweet_count += 1
      self.recent_tweets.appendleft(tweet)
      if len(self.recent_tweets) > 5:
        self.recent_tweets.pop()

