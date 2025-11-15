import json
from typing import Callable, List, Optional, Dict

from fastapi import HTTPException, Request, Response

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Scope, ASGIApp, Receive, Send

from common.aws.kms import decrypt
from common.crypto.aes import aes_encrypt, aes_decrypt
from common.crypto.rsa import rsa_encrypt

from ..schemas.request import EncryptedRequest, EncryptedResponse, EncryptedResponseData

class EncryptResponseMiddleware(BaseHTTPMiddleware):
    """
        Middleware to encrypt responses With Client Public Key.
    """
    skip_routes: List[str] = []
    redis_storage: Optional[object] = None
    internal_storage: Optional[Dict[str, str]] = None

    def __init__(self, app, redis_storage: Optional[object] = None, internal_storage: Optional[Dict[str, str]] = None, skip_routes: List[str] = []):
        super().__init__(app)
        self.skip_routes = skip_routes
        self.redis_storage = redis_storage
        self.internal_storage = internal_storage

        if redis_storage is None and internal_storage is None:
            raise ValueError("Either redis_storage or internal_storage must be provided")

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        session_id = request.cookies.get("session_id")
        
        if not session_id:
            print("Session ID not found in cookies")
            raise HTTPException(status_code=500, detail="Internal Server Error")

        # Determine if encryption should be skipped
        skip_encryption = (
            not session_id or any(request.url.path.endswith(path) for path in self.skip_routes)
        )
        if skip_encryption:
            return response

        try:
            # Retrieve the frontend public key
            if self.redis_storage:
                pubkey_fe = await self.redis_storage.get(session_id)
                if pubkey_fe is None:
                    return response
                if isinstance(pubkey_fe, bytes):
                    pubkey_fe = pubkey_fe.decode()
            else:
                pubkey_fe = self.internal_storage.get(session_id)
                if not pubkey_fe:
                    return response

            # Collect original response body (sent as stream)
            body_bytes = b""
            async for chunk in response.body_iterator:
                body_bytes += chunk

            parsed_body = json.loads(body_bytes)

            # --- Encrypt data with AES Key ---
            aes_result = aes_encrypt(parsed_body)  # auto-generates key + IV

            # --- Encrypt AES key with RSA ---
            encrypted_key_b64 = rsa_encrypt(pubkey_fe, aes_result["aes_key"])

            # --- Build payload ---
            payload = EncryptedResponse(
                data=EncryptedResponseData(
                    ciphertext=aes_result["ciphertext"],
                    iv=aes_result["iv"],
                    tag=aes_result["tag"],
                ),
                key=encrypted_key_b64,
            )

            # Return NEW JSON response
            return Response(
                content=json.dumps(payload.model_dump(mode="json")),
                status_code=response.status_code,
                media_type="application/json",
                headers={k: v for k, v in response.headers.items() if k.lower() != "content-length"},
            )

        except Exception as e:
            print(f"Failed to encrypt response: {e}")
            return response

class DecryptRequestMiddleware:
    """
        Middleware to decrypt encrypted requests With AWS Key Management Service.
    """
    def __init__(self, app: ASGIApp, boto3_client_dep: Callable, key_id: str, algorithm, skip_routes=None):
        self.app = app
        self.boto3_client_dep = boto3_client_dep
        self.key_id = key_id
        self.algorithm = algorithm
        self.skip_routes = skip_routes or []

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if any(path.endswith(p) for p in self.skip_routes):
            await self.app(scope, receive, send)
            return

        # Capture body
        body = b""
        more_body = True

        async def inner_receive():
            nonlocal body, more_body
            message = await receive()
            if message["type"] == "http.request":
                body += message.get("body", b"")
                more_body = message.get("more_body", False)
            return message

        while more_body:
            await inner_receive()

        if not body:
            await self.app(scope, receive, send)
            return

        try:
            payload_dict = json.loads(body)
            payload = EncryptedRequest(**payload_dict)

            # --- Decrypt AES key using KMS ---
            boto3_client = self.boto3_client_dep()
            aes_key_bytes = await decrypt(
                boto3_client=boto3_client,
                key_id=self.key_id,
                ciphertext_b64=payload.key,
                alg=self.algorithm
            )

            # --- AES Decrypt the request data ---
            decrypted = aes_decrypt(
                aes_key=aes_key_bytes,
                ciphertext_b64=payload.data.ciphertext,
                iv_b64=payload.data.iv,
                tag_b64=payload.data.tag,
                as_json=True
            )

            decrypted_json = json.dumps(decrypted).encode("utf-8")

        except Exception as e:
            from fastapi.responses import JSONResponse
            response = JSONResponse({"detail": f"Decryption failed: {str(e)}"}, status_code=400)
            await response(scope, receive, send)
            return

        # Replace receive with decrypted body
        async def receive_decrypted():
            return {"type": "http.request", "body": decrypted_json, "more_body": False}

        await self.app(scope, receive_decrypted, send)
