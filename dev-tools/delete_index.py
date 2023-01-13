import argparse

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


parser = argparse.ArgumentParser()
parser.add_argument(
    "--endpoint",
    help="Opensearch endpoint of the index to delete."
)
parser.add_argument("--index", help="Target index to delete")
parser.add_argument("--region", help="AWS Region of the endpoint to delete")
args = parser.parse_args()

credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region=args.region)
client = OpenSearch(
    hosts=[{'host':  args.endpoint, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
client.indices.delete(
    args.index
)
