from pydantic import BaseModel, ConfigDict

class JWTClaims(BaseModel):
    sub: str
    pur: str
    jti: str
    iat: float
    exp: float
    pld: dict

    model_config = ConfigDict(from_attributes=True, extra="forbid")