import base64
from typing import Any

from .constants import KMSAlgorithm

async def fetch_pubkey(client: Any, key_id: str) -> str:
    response = client.get_public_key(KeyId=key_id)
    public_key_der = response["PublicKey"]

    # Convert DER → PEM
    public_key_b64 = base64.b64encode(public_key_der).decode("utf-8")
    public_key_pem = "-----BEGIN PUBLIC KEY-----\n"
    public_key_pem += "\n".join(
        [public_key_b64[i:i + 64] for i in range(0, len(public_key_b64), 64)]
    )
    public_key_pem += "\n-----END PUBLIC KEY-----"

    return public_key_pem

async def encrypt(
    boto3_client: Any,
    key_id: str,
    plaintext: str,
    alg: KMSAlgorithm,
) -> str:
    response = boto3_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext.encode("utf-8"),
        EncryptionAlgorithm=alg
    )
    
    return base64.b64encode(response["CiphertextBlob"]).decode("utf-8")

async def decrypt(
    boto3_client: Any,
    key_id: str,
    ciphertext_b64: str,
    alg: KMSAlgorithm,
) -> bytes:
    
    # Base64 decode ciphertext
    ciphertext_blob = base64.b64decode(ciphertext_b64)
    
    # Call KMS decrypt
    response = boto3_client.decrypt(
        KeyId=key_id,
        CiphertextBlob=ciphertext_blob,
        EncryptionAlgorithm=alg,
    )
    
    # Return raw AES key bytes (do NOT decode UTF-8)
    return response["Plaintext"]