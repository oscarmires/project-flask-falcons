#!/bin/bash

CONTENT=$( $RANDOM | md5sum )

POST_ID=$( curl -X POST http://localhost:5000/api/timeline_post -d "name=Oscar&email=oscar-me@outlook.com&content=$CONTENT" | jq --raw-output '.id' )
RES=$( curl http://localhost:5000/api/timeline_post | jq --raw-output '.timeline_posts[] | "\(.content)"' )

if [[ $RES == *$CONTENT* ]]; then
  echo "API POST test passed"
else
  echo "API POST test failed"
fi

curl -X DELETE http://localhost:5000/api/timeline_post -d "id=$POST_ID"
