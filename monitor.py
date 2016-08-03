import collections
import copy
import datetime
import flask
import humanize
import json
import rethinkdb as r
import threading

from flags import flags

class Monitor(object):
  def __init__(self):
    self.lock = threading.Lock()

    self.recent_tweets = collections.deque()
    self.start_time = datetime.datetime.now()
    self.db_connection = r.connect(password=flags.password)
    self.server = self.make_server()
    self.thread = threading.Thread(
      target=self.server.run,
      kwargs={"host": "0.0.0.0"},
      daemon=True,
    )

    self.thread.start()

  def record_tweet(self, tweet):
    tweet = copy.copy(tweet)
    tweet["timestamp"] = str(tweet["timestamp"])
    print(json.dumps(tweet, indent=4, sort_keys=True))

    with self.lock:
      self.recent_tweets.appendleft(tweet)
      if len(self.recent_tweets) > 5:
        self.recent_tweets.pop()

  def tweet_count(self):
    return r.db(flags.database).table(flags.table).count().run(self.db_connection)

  def uptime(self):
    return datetime.datetime.now() - self.start_time

  def make_server(self):
    app = flask.Flask(__name__)

    @app.route("/")
    def index():
      html = []
      html.append("<b>Started:</b> %s<br>" % humanize.naturaltime(self.uptime()))
      html.append("<b>Tweets:</b> %s<br>" % self.tweet_count())

      with self.lock:
        html.append("<pre>")
        for tweet in self.recent_tweets:
          html.append(json.dumps(tweet, indent=4, sort_keys=True))
        html.append("</pre>")

      return "\n".join(html)

    @app.route("/stats/count")
    def count():
      return str(self.tweet_count())

    @app.route("/stats/uptime")
    def uptime():
      return str(self.uptime())

    return app
