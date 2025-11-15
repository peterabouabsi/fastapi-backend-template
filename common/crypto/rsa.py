from typing import Optional, Union

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# KEY MANAGEMENT
def generate_rsa_keypair(key_size: int = 2048) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """
    Generate a new RSA private/public key pair.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    return private_key, private_key.public_key()

def serialize_private_key(private_key, password: Optional[bytes] = None) -> bytes:
    """
    Serialize private key into PEM bytes (optionally password-protected).
    """
    encryption_algorithm = (
        serialization.BestAvailableEncryption(password)
        if password else serialization.NoEncryption()
    )
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm,
    )


def serialize_public_key(public_key) -> bytes:
    """
    Serialize public key into PEM bytes.
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def load_private_key(pem: Union[str, bytes], password: Optional[bytes] = None) -> rsa.RSAPrivateKey:
    """
    Load private key from PEM string or bytes.
    """
    if isinstance(pem, str):
        pem = pem.encode()
    return serialization.load_pem_private_key(pem, password=password)


def load_public_key(pem: Union[str, bytes]) -> rsa.RSAPublicKey:
    """
    Load public key from PEM string or bytes.
    """
    if isinstance(pem, str):
        pem = pem.encode()
    return serialization.load_pem_public_key(pem)

# ENCRYPTION / DECRYPTION
def rsa_encrypt(plaintext: bytes, public_key: Union[str | bytes | rsa.RSAPublicKey]) -> bytes:
    """
    Encrypt plaintext with RSA public key using OAEP + SHA-256.
    """
    if isinstance(public_key, str) or isinstance(public_key, bytes):
        public_key = load_public_key(public_key)

    return public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

def rsa_decrypt(ciphertext: bytes, private_key: Union[str | bytes | rsa.RSAPrivateKey]) -> bytes:
    """
    Decrypt ciphertext with RSA private key using OAEP + SHA-256.
    """
    if isinstance(private_key, str) or isinstance(private_key, bytes):
        private_key = load_private_key(private_key)
    
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

