#!/bin/bash
# Use these shell code instead of the Twitter API (too slow and have to sleep for a while after some times crawlers)


curl "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary" \
-G \
--data-urlencode 'start_key=["melbourne",2018,3,1]' \
--data-urlencode 'end_key=["melbourne",2018,7,1]' \
--data-urlencode 'reduce=false' \
--data-urlencode 'include_docs=true' \
--user "readonly:ween7ighai9gahR6" \
-o /vol1/twitter_0301_0701.json

curl "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary" \
-G \
--data-urlencode 'start_key=["melbourne",2017,8,1]' \
--data-urlencode 'end_key=["melbourne",2018,2,28]' \
--data-urlencode 'reduce=false' \
--data-urlencode 'include_docs=true' \
--user "readonly:ween7ighai9gahR6" \
-o /vol1/twitter_17_0228.json


