import json

from botocore.exceptions import ClientError

# global services
from common.aws import create_session, create_client

session = create_session()
client = create_client(session, 'secretsmanager', 'eu-central-1')

async def fetch_secrets(secret_id: str):
    try:
        response = client.get_secret_value(SecretId=secret_id)
        secret = json.loads(response['SecretString'])
        return secret
    except ClientError as e:
        raise RuntimeError(f"Failed to fetch secret '{secret_id}': {e}") from e

def get_secrets_client():
    return client