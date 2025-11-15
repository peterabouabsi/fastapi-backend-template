import base64
from typing import Optional

from .rsa import rsa_encrypt, rsa_decrypt, load_public_key, load_private_key
from .aes import generate_aes_key, aes_encrypt, aes_decrypt

# HYBRID ENCRYPT
def hybrid_encrypt(
    public_key_pem: str, 
    plaintext: bytes,
    aes_key: Optional[bytes] = None
) -> dict:
    """
    Encrypts a message using AES-GCM and wraps the AES key with RSA.
    Returns base64-encoded encrypted key, ciphertext, nonce, tag.
    """
    public_key = load_public_key(public_key_pem)

    # Generate AES key
    aes_key = aes_key or generate_aes_key()

    # Encrypt message with AES
    aes_result = aes_encrypt(plaintext, aes_key)

    # Encrypt AES key with RSA
    encrypted_key = rsa_encrypt(aes_key, public_key)

    return {
        "encrypted_aeskey": base64.b64encode(encrypted_key).decode(),
        "ciphertext": aes_result["ciphertext"],
        "nonce": aes_result["nonce"],
        "tag": aes_result["tag"]
    }

# HYBRID DECRYPT
def hybrid_decrypt(
    private_key_pem: str, 
    data: dict
) -> bytes:
    """
    Decrypts a hybrid encrypted message using RSA private key and AES-GCM.
    Expects base64-encoded encrypted_key, ciphertext, nonce, tag.
    """
    if not hasattr(data, "encrypted_aeskey"):
        raise Exception("Key 'encrypted_aeskey' is missing.")
    
    private_key = load_private_key(private_key_pem)

    # Decrypt AES key with RSA
    encrypted_key = base64.b64decode(data["encrypted_key"])
    
    aes_key = rsa_decrypt(encrypted_key, private_key)

    # Decrypt message with AES
    plaintext = aes_decrypt(
        ciphertext_b64=data["ciphertext"],
        key=aes_key,
        nonce_b64=data["nonce"],
        tag_b64=data["tag"]
    )
    return plaintext
