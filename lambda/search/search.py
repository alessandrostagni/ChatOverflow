import json
import os
import requests

# Elasticsearch endpoint
ES_ENDPOINT = os.environ['ES_ENDPOINT']

# Elasticsearch index to search in
ES_INDEX = os.environ['ES_INDEX']

def lambda_handler(event, context):
    # Get the search query from the event
    query = event["queryStringParameters"]["q"]

    # Construct the Elasticsearch search request
    data = {
        "query": {
            "fuzzy": {
                "field": "text",
                "value": query
            }
        }
    }
    headers = { "Content-Type": "application/json" }
    url = f"{ES_ENDPOINT}/{ES_INDEX}/_search"
    response = requests.post(url, headers=headers, json=data)
    
    # Check for errors
    response.raise_for_status()
    
    # Return the search results
    return {
        "statusCode": 200,
        "body": json.dumps(response.json()["hits"])
    }
