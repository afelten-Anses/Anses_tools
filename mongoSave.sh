#!/bin/sh

prefix="/mnt/NAS/NASBIO1/SAVE/mongoDB/"
jour=$(date +%Y%m%d)
suffix=".gz"

mongodump -d GAMeRdb -u Kindle -p Amazon -o $prefix$jour
