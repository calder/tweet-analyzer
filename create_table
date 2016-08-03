#!/usr/bin/env python3

import argparse
import rethinkdb

parser = argparse.ArgumentParser(description="Create a tweet table.")
parser.add_argument("--database", required=True)
flags = parser.parse_args()

rethinkdb.connect().repl()
rethinkdb.db_create(flags.database)
rethinkdb.db(flags.database).table_create("tweets")
