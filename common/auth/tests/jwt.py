import asyncio

from pydantic import BaseModel

from common.auth.jwt import (
    token_sign, 
    token_encrypt, 
    token_sign_encrypt, 
    token_decrypt, 
    token_verify, 
    token_decrypt_verify
)
from common.auth.dependencies.authorize import authorize
from common.auth.schemas.context import AuthContext

class SignInPayload(BaseModel):
    email: str
    password: str

signing_key = "secret"
signing_alg = "HS256"
decryption_key = "Rtm9Wgdy_8SvXM1w48WjKNaC-HQBMqPccknmucV89Uk="
payload = { "sub": "email", "purpose": "signin", "pur": "access_token" }

# Token sign
signed_token_1 = asyncio.run(
    token_sign(
        payload=payload,
        key=signing_key,
        alg=signing_alg,
        minutes=1
    )
)

# Token encrypt
encrypted_token_1 = asyncio.run(
    token_encrypt(
        token=signed_token_1,
        key=decryption_key
    )
)

# Token sign + encrypt
encrypted_signed_token_1 = asyncio.run(
    token_sign_encrypt(
        payload=payload,
        key=signing_key,
        minutes=30,
        alg=signing_alg,
        encryption_key=decryption_key,
    )
)

# in routes
auth_context_1: AuthContext = authorize(key=signing_key, alg=signing_alg, decryption_key=decryption_key)

print({
    "token_sign": signed_token_1,
    "token_encrypt": encrypted_token_1,
    "token_sign_encrypt": encrypted_signed_token_1,
    "auth_context_1": auth_context_1
})

print("="*60, "\n")
print("="*60, "\n")

# Token decrypt
decrypted_signed_token = asyncio.run(
    token_decrypt(
        token=encrypted_token_1,
        key=decryption_key,
    )
)

# Token verify
auth_context_21 = asyncio.run(
    token_verify(
        token=decrypted_signed_token,
        key=signing_key,
        algs=[signing_alg]
    )
)
# Token decrypt + verify
auth_context_22 = asyncio.run(
    token_decrypt_verify(
        token=encrypted_token_1,
        key=signing_key,
        algs=[signing_alg],
        decryption_key=decryption_key,
    )
)

print({
    "decrypted_signed_token": decrypted_signed_token,
    "auth_context_21": auth_context_21,
    "auth_context_22": auth_context_22
})