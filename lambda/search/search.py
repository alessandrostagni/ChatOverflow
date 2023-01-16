import os
import json

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


# Elasticsearch endpoint
ES_ENDPOINT = os.environ['ES_ENDPOINT']

# Elasticsearch index to search in
ES_INDEX = os.environ['ES_INDEX']


def get_client():
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, 'ap-southeast-2')

    client = OpenSearch(
        hosts=[{'host':  ES_ENDPOINT, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    return client

def get_documents_by_query(client, query):
    # Construct the Elasticsearch search request
    query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["text"],
                "fuzziness":"AUTO"
            }
        }
    }
    response = client.search(
        body=query,
        index=ES_INDEX
    )

    # Return the search results
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "content-type": "application/json"
        },
        "body": json.dumps([{
                "id": h['_id'],
                "text": h['_source']['text'],
                "full_convo_s3_key": h['_source']['full_convo_s3_key']
            } for h in response['hits']['hits']
        ])
    }

def get_document_by_s3_file(client, s3_file):
    s3 = boto3.client('s3')
    uri_without_prefix = s3_file.replace("s3://", "")
    bucket = uri_without_prefix.split('/')[0]
    key = '/'.join(uri_without_prefix.split('/')[1:])
    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode("utf-8")
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "content-type": "application/json"
        },
        "body": json.dumps({
            "text": data
        })
    }

def bad_request():
    return {
        "isBase64Encoded": False,
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "content-type": "application/json"
        },
        "body": "Bad Request."
    }

def lambda_handler(event, context):
    # Get the search query from the event
    if 'q' in event["queryStringParameters"]:
        query = event["queryStringParameters"]["q"]
        client = get_client()
        return get_documents_by_query(client, query)
    elif 's3_file' in event["queryStringParameters"]:
        doc_id = event["queryStringParameters"]["s3_file"]
        client = get_client()
        return get_document_by_s3_file(client, doc_id)
    return bad_request()
