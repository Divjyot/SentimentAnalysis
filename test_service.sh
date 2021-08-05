#! /usr/bin/env bash

# Declare Service URL to test
API_URL=http://localhost:80

# Helper to create request body
generate_post_data()
{
cat <<END
{
  "query": "$1"
}
END
}

# Helper to perform POST
function post_query_to_api() {
      req_body=$(generate_post_data "$1")
      
      echo "POST BODY: ${req_body}"
      curl -X POST "${API_URL}/predict" \
      --header 'Content-Type: application/json'\
      --header 'Secret-Key: dev'\
      --data "${req_body}"
}

echo "1. Checking API is up?"
echo "$(curl -X GET ${API_URL})"
echo "-------------------------"

echo "2. Performing Senitment analysis for"
if [ -z "$1" ]
then
      echo "No string arg provided - Running Demo"

      pos_query='This challenge is terrifying!'
      echo "Positive Sentiment :'${pos_query}'"
      post_query_to_api "${pos_query}" 

      echo "----------------------------------"

      neg_query='This challenge is lots of fun!'
      echo "Negative Sentiment : '${neg_query}'"
      post_query_to_api "${neg_query}" 
else
      echo ": '$1'"
      post_query_to_api "$1"
fi