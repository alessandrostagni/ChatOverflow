import boto3
import os

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


# Initialize boto3 S3 client and Elasticsearch client
ES_ENDPOINT = os.environ['ES_ENDPOINT']
ES_INDEX = os.environ['ES_INDEX']
s3 = boto3.client('s3')
convo_delimiter = '\n--------------------------\n'
chunks_length = 4


def create_index(client, es_endpoint, es_index):
    body = {
        "mappings": {
            "properties": {
                "text": {"type": "text", "analyzer": "english"}
            }
        }
    }
    client.index(index=es_index, body=body)


def split_conversation(data):
    chunks = data.split(convo_delimiter)
    chunks = [chunks[x:x+chunks_length] for x in range(0, len(chunks), 100)]
    return chunks


def lambda_handler(event, context):
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, 'ap-southeast-2')
    client = OpenSearch(
        hosts=[{'host':  ES_ENDPOINT, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
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
        # Get conversation chunks to be indexed
        chunks = split_conversation(data.decode("utf-8"))
        # Index chunks
        for chunk in chunks:
            index_data = {
                'text': convo_delimiter.join(chunk),
                'full_convo_s3_key': f's3://{bucket}/{key}'
            }
            client.index(index=ES_INDEX, body=index_data)
    except Exception as e:
        print(e)
        raise e
