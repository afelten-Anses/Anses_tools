#!/bin/sh

prefix="/global/bio/save/Redmine/"
jour=$(date +%Y%m%d)
suffix=".tar.gz"

tar -czf $prefix$jour$suffix /opt/redmine-3.2.0-2
