import boto3
import os

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


# Initialize boto3 S3 client and Elasticsearch client
ES_ENDPOINT = os.environ['ES_ENDPOINT']
ES_INDEX = os.environ['ES_INDEX']
s3 = boto3.client('s3')

def create_index(client, es_endpoint, es_index):
    body = {
        "mappings":{
            "properties": {
                "text": {"type": "text", "analyzer": "english"}
            }
        }
    }
    client.index(index=es_index, body=body)

def lambda_handler(event, context):
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, 'ap-southeast-2')
    client = OpenSearch(
        hosts = [{'host':  ES_ENDPOINT, 'port': 443}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    create_index(client, ES_ENDPOINT, ES_INDEX)

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
        client.index(index=ES_INDEX, body=parsed_data)
    except Exception as e:
        print(e)
        raise e
