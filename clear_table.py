#!/usr/bin/env python3

import argparse
import rethinkdb

parser = argparse.ArgumentParser(description="Clear a tweet table.")
parser.add_argument("--database", required=True)
flags = parser.parse_args()

rethinkdb.connect().repl()
rethinkdb.db(flags.database).table("tweets").delete().run()
