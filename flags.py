import argparse

parser = argparse.ArgumentParser(
  description="Download live tweets on a topic.",
)

parser.add_argument("--consumer_key", required=True)
parser.add_argument("--consumer_secret", required=True)
parser.add_argument("--access_token_key", required=True)
parser.add_argument("--access_token_secret", required=True)
parser.add_argument("--password")
parser.add_argument("--database", required=True)
parser.add_argument("--table", default="tweets")
parser.add_argument("--filter", required=True, nargs="+")

flags = parser.parse_args()
