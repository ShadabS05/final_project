#!/bin/sh
#
files=$(find data/*)
echo '================================================================================'
echo 'load pg_normalized_batch'
echo '================================================================================'
time echo "$files" | parallel python3 -u load_tweets_dev.py --db postgresql://hello_flask:hello_flask@localhost:3067/hello_flask_dev --input
