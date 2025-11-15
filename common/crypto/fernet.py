import json
from typing import Any, Union

from cryptography.fernet import Fernet, InvalidToken
from fastapi import HTTPException

def generate_fernet_key(to_str: bool = False) -> bytes:
    key: bytes = Fernet.generate_key()
    if to_str:
        return key.decode()
    return key

async def encrypt_data(data: Any, key: Union[str, bytes]) -> str:
    try:
        if isinstance(key, str):
            key = key.encode()
        f = Fernet(key)
        plaintext_bytes = json.dumps(data).encode()
        token = f.encrypt(plaintext_bytes)
        return token.decode()
    except Exception as e:
        raise HTTPException(500, f"Encryption failed at exact point: {e}")


async def decrypt_data(data: str, key: Union[str, bytes]) -> Any:
    try:
        if isinstance(key, str):
            key = key.encode()
        f = Fernet(key)
        plaintext_bytes = f.decrypt(data.encode())
        return json.loads(plaintext_bytes)
    except InvalidToken:
        raise HTTPException(500, f"Invalid token / wrong key: {data}")
    except Exception as e:
        raise HTTPException(500, f"Decryption failed at exact point: {e}")