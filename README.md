## Setup

1. [Install](https://www.rethinkdb.com/docs/install/) and [start](https://www.rethinkdb.com/docs/start-a-server/) RethinkDB.

2. Install Pip:
  ```sh
  sudo apt-get install python3-pip
  ```

3. Install Python libraries:
  ```sh
  sudo pip3 install flask humanize python-twitter pytz rethinkdb
  ```

4. Create the table to store tweets in:
  ```sh
  python3 setup_table.py --database BLM
  ```

5. Obtain Twitter [Application Owner Access Tokens](https://dev.twitter.com/oauth/overview/application-owner-access-tokens).

## Running

  ```sh
  ./collect.sh \
    --consumer_key YOUR_TWITTER_CONSUMER_KEY \
    --consumer_secret YOUR_TWITTER_CONSUMER_SECRET \
    --access_token_key YOUR_TWITTER_ACCESS_TOKEN_KEY \
    --access_token_secret YOUR_TWITTER_ACCESS_TOKEN_SECRET \
    --database BLM \
    --filter '#blacklivesmatter'
  ```

This will dump all tweets matching your filter into the `tweets` table of the database you specified.
