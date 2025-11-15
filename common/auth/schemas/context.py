from pydantic import BaseModel

class AuthContext(BaseModel):
    sub: str
    jti: str
    pld: dict