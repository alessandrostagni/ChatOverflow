import json
import boto3
import os

import requests


# Initialize boto3 S3 client and Elasticsearch client
ES_ENDPOINT = os.environ['ES_ENDPOINT']
ES_INDEX = os.environ['ES_INDEX']
s3 = boto3.client('s3')

def create_index(es_endpoint, es_index):
    index_exists = requests.head(f"{es_endpoint}/{es_index}").status_code == 200
    if not index_exists:
        # Create index with desired settings and mappings
        index_settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            }
        }
        requests.put(f"{es_endpoint}/{es_index}", json=index_settings)

def lambda_handler(event, context):
    create_index(ES_ENDPOINT, ES_INDEX)
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    try:
        # Get the object from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        # Read the file
        data = response['Body'].read()
        # Your parse code here
        # parsed_data = json.loads(data) # or any other parsing method
        parsed_data = {'text': str(data)}
        # Index the parsed data
        requests.put(f"{ES_ENDPOINT}/{ES_INDEX}/_doc/", json=parsed_data)
    except Exception as e:
        print(e)
        raise e
