#!/bin/bash

cd "`dirname "$0"`"

while [ 1 ]; do
  python3 collect.py $@ 2>> STDERR
  echo "collect.py exited, restarting in 10s..."
  sleep 10
done
