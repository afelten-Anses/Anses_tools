#!/bin/sh

prefix="/global/bio/save/mongoDB/"
jour=$(date +%Y%m%d)
suffix=".gz"

mongodump -d GAMeRdb -u Kindle -p Amazon -o $prefix$jour
