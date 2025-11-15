from datetime import datetime, timedelta, timezone
from typing import Callable, List, Union
from uuid import uuid4

from fastapi import HTTPException

from jose import JWTError
from jose.constants import Algorithms

from ..common.crypto.fernet import encrypt_data, decrypt_data

# schemas
from ..schemas.claims import JWTClaims

# utils
from ..utils.resolvers import resolve_key

# jwt
from .jwt import sign, verify

async def token_sign(payload: dict, key: str, alg: Algorithms, minutes: int) -> str:
    if "sub" not in payload:
        raise Exception("Missing subject claim. 'pur' is required.")
    if "pur" not in payload:
        raise Exception("Missing purpose claim. 'pur' is required.")
    
    sub = str(payload["sub"])
    pur = str(payload["pur"])
    now = datetime.now(tz=timezone.utc)
    exp = (now + timedelta(minutes=minutes)).timestamp()
    iat = int(now.timestamp())
    jti = str(uuid4())

    if "role_ids" not in payload:
        payload["role_ids"] = []

    claims = JWTClaims(sub=sub, pur=pur, exp=exp, iat=iat, jti=jti, pld=payload)
    claims_dict = claims.model_dump()

    return await sign(claims=claims_dict, key=key, alg=alg)

async def token_encrypt(token: str, key: Union[str, Callable[..., str]]) -> str:
    encryption_key: str = key
    if isinstance(key, Callable):
        encryption_key = await resolve_key(key)

    return await encrypt_data(data=token, key=encryption_key)

async def token_sign_encrypt(
    payload: dict,
    key: str,
    minutes: int,
    alg: Algorithms,
    encryption_key: Union[str, Callable[..., str]]
) -> str:
    signed_jwt = await token_sign(payload=payload, key=key, minutes=minutes, alg=alg)
    encrypted_jwt = await token_encrypt(token=signed_jwt, key=encryption_key)
    return encrypted_jwt

async def token_decrypt(token: str, key: Union[str, Callable[..., str]]) -> str:
    decryption_key: str = key
    if isinstance(key, Callable):
        decryption_key = await resolve_key(key)
    
    return await decrypt_data(data=token, key=decryption_key)

async def token_verify(token: str, key: str, algs: List[Algorithms]) -> dict:
    return await verify(token=token, key=key, algs=algs)

async def token_decrypt_verify(
    token: str,
    key: str,
    algs: List[Algorithms],
    decryption_key: Union[str, Callable[..., str]]
) -> dict:
    try:
        signed_token = await token_decrypt(token=token, key=decryption_key)
        claims = await token_verify(token=signed_token, key=key, algs=algs)
        return claims

    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected verification error: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized.")

async def token_validate(claims: dict, purpose: str) -> bool:
    try:
        jti = claims.get("jti")
        payload = claims.get("payload", {})

        if not jti or payload.get("purpose") != purpose:
            return False

        # Optional: check blacklist or revoked token store here
        return True

    except Exception as e:
        print(f"Unexpected validation error: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized.")