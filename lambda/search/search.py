import os
import json

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


# Elasticsearch endpoint
ES_ENDPOINT = os.environ['ES_ENDPOINT']

# Elasticsearch index to search in
ES_INDEX = os.environ['ES_INDEX']

def lambda_handler(event, context):
    # Get the search query from the event
    print(event)
    query = event["queryStringParameters"]["q"]

    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, 'ap-southeast-2')

    client = OpenSearch(
        hosts = [{'host':  ES_ENDPOINT, 'port': 443}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    # Construct the Elasticsearch search request
    query = {
        "query": {
            "fuzzy": {
                "text": query
            }
        }
    }
    response = client.search(
        body = query,
        index = ES_INDEX
    )
    print(response['hits']['hits'])

    # Return the search results
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "content-type": "application/json"
        },
        "body": json.dumps([h['_source']['text'] for h in response['hits']['hits']])
    }
