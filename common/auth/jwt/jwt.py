from typing import List

from fastapi import HTTPException

from jose import jwt
from jose.constants import Algorithms

async def sign(claims: dict, key: str, alg: Algorithms) -> str:
    try:
        token = jwt.encode(claims=claims, key=key, algorithm=alg)
        return token
    except Exception as e:
        print(f"JWT signing error: {e}")
        raise HTTPException(401)

async def verify(token: str, key: str, algs: List[Algorithms]) -> dict:
    try:
        payload = jwt.decode(token=token, key=key, algorithms=algs)
        return payload
    except Exception as e:
        print(f"JWT verification error: {e}")
        raise HTTPException(401)
    