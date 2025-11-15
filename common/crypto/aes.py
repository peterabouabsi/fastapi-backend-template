import os
import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# AES KEY GENERATION
def generate_aes_key(length: int = 32) -> bytes:
    """
    Generate a random AES key.
    length: 16 -> AES-128, 32 -> AES-256
    """
    return os.urandom(length)

# ENCRYPTION
def aes_encrypt(plaintext: bytes, key: bytes, nonce: bytes = os.urandom(12)) -> dict:
    """
    Encrypt plaintext using AES-GCM.
    # 96-bit nonce recommended for GCM
    Returns dict with base64 encoded ciphertext, nonce, tag.
    """

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "tag": base64.b64encode(encryptor.tag).decode()
    }

# DECRYPTION
def aes_decrypt(ciphertext_b64: str, key: bytes, nonce_b64: str, tag_b64: str) -> bytes:
    """
    Decrypt AES-GCM encrypted ciphertext.
    """
    ciphertext = base64.b64decode(ciphertext_b64)
    nonce = base64.b64decode(nonce_b64)
    tag = base64.b64decode(tag_b64)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext