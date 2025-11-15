from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from typing import Optional

class HTTPBearer401(HTTPBearer):
    """
    Custom HTTPBearer that returns 401 on missing or invalid credentials,
    and logs unauthorized access attempts.
    """

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        try:
            credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)

            if not credentials:
                raise HTTPException(status_code=401, detail="Unauthorized")
            
            return credentials

        except HTTPException as he:
            # Convert any default 403 from HTTPBearer to 401
            if he.status_code == 403:
                print(f"Unauthorized access attempt from {request.client.host}")
                raise HTTPException(status_code=401, detail="Unauthorized")
            # Re-raise other HTTPExceptions
            raise he