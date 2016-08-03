#!/usr/bin/env python3

import argparse
import rethinkdb
import twitter

parser = argparse.ArgumentParser(
  description="Download live tweets on a topic.",
)

parser.add_argument("--consumer_key", required=True)
parser.add_argument("--consumer_secret", required=True)
parser.add_argument("--access_token_key", required=True)
parser.add_argument("--access_token_secret", required=True)
parser.add_argument("--database", required=True)
parser.add_argument("--filter", required=True, nargs="+")

flags = parser.parse_args()

rethinkdb.connect().repl()
db = rethinkdb.db(flags.database)
tweets = db.table("tweets")

api = twitter.Api(
  consumer_key=flags.consumer_key,
  consumer_secret=flags.consumer_secret,
  access_token_key=flags.access_token_key,
  access_token_secret=flags.access_token_secret,
)

stream = api.GetStreamFilter(track=flags.filter)

for tweet in stream:
  row = {
    "followers": tweet["user"]["followers_count"],
    "text": tweet["text"],
    "user": tweet["user"]["name"],
  }
  tweets.insert([row]).run()
  print(row)
