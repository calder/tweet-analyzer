#!/usr/bin/env python3

import datetime
import pytz
import rethinkdb as r
import twitter

from flags import flags
from monitor import Monitor

monitor = Monitor()

db_connection = r.connect()
table = r.db(flags.database).table(flags.table)

api = twitter.Api(
  consumer_key=flags.consumer_key,
  consumer_secret=flags.consumer_secret,
  access_token_key=flags.access_token_key,
  access_token_secret=flags.access_token_secret,
)

stream = api.GetStreamFilter(track=flags.filter)

for tweet in stream:
  row = {
    "timestamp": pytz.utc.localize(datetime.datetime.utcfromtimestamp(int(tweet["timestamp_ms"]) / 1000.0)),
    "followers": tweet["user"]["followers_count"],
    "text": tweet["text"],
    "user": tweet["user"]["name"],
  }
  table.insert([row]).run(db_connection)
  monitor.record_tweet(row)
