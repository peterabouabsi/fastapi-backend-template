from typing import Callable, List, Union, Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials

# jwt
from ..jwt import token_decrypt_verify, token_verify

# schemas
from ..schemas.claims import JWTClaims
from ..schemas.context import AuthContext

# security
from ..security import HTTPBearer401

# utils
from ..utils.resolvers import resolve_key

bearer_scheme = HTTPBearer401()

def authorize(
    key: Union[str, Callable[..., str]],
    alg: str,
    decryption_key: Optional[Union[str, Callable[..., str]]] = None,
    role_ids: Optional[List[List[str]]] = None # Optional role permissions supporting AND/OR e.g.: [ ["admin"], ["user", "editor"] ]
):
    
    if role_ids is None:
        role_ids = []
    
    async def _dependency(
        _: Request,
        authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme)
    ):
        # Resolve key dynamically
        verification_key = key
        if callable(key):
            verification_key = await resolve_key(key)

        # Extract token
        token = authorization.credentials

        # Choose handler based on presence of decryption_config
        claims: JWTClaims = await __handle_verification(
            token=token, 
            verification_key=verification_key, 
            alg=alg, 
            decryption_key=decryption_key
        )
        
        sub: str = claims.sub
        pld: dict = claims.pld
        jti: str = claims.jti

        # validate token blacklist
        await __handle_blacklist()

        # verify role permissions
        if len(role_ids) > 0:
            await __handle_roles(token_pld=pld, role_ids=role_ids)

        return AuthContext(sub=sub, pld=pld, jti=jti)

    return Depends(_dependency)

async def __handle_verification(token: str, verification_key: str, alg: str, decryption_key: Optional[Union[str, Callable[..., str]]] = None):
    claims: dict = {}
    if decryption_key:
        claims = await token_decrypt_verify(
            token=token,
            key=verification_key,
            algs=[alg],
            decryption_key=decryption_key
        )
    else:
        claims = await token_verify(
            token=token,
            key=verification_key,
            algs=[alg]
        )
    
    return JWTClaims(**claims)

async def __handle_blacklist():
    pass

async def __handle_roles(token_pld, role_ids):
    def check_roles(token_roles: List[str]) -> bool:
        token_roles_set = set(token_roles)
        for and_group_list in role_ids:
            if all(role in token_roles_set for role in and_group_list):
                return True # At least one AND group matches
        return False # No group matched
    
    if not check_roles(token_pld["role_ids"]):
        raise HTTPException(status_code=403, detail="Forbidden. You do not have access to this resource.")