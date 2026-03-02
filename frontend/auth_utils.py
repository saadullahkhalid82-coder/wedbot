from typing import Dict, Any
from jose import jwt
from jose.exceptions import JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests


SUPABASE_URL: str = "https://agglgrfstvugdzoqyepv.supabase.co"
ALGORITHM: str = "RS256"

JWKS_URL: str = f"{SUPABASE_URL}/auth/v1/keys"

security = HTTPBearer()
JWKS_CACHE: Dict[str, Any] = {}


def _get_jwks() -> Dict[str, Any]:
    global JWKS_CACHE

    if JWKS_CACHE:
        return JWKS_CACHE

    response = requests.get(JWKS_URL, timeout=10)
    response.raise_for_status()

    JWKS_CACHE = response.json()
    return JWKS_CACHE


def verify_supabase_jwt(token: str) -> Dict[str, Any]:
    try:
        jwks = _get_jwks()
        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=[ALGORITHM],
            audience="authenticated",
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:

    token: str = credentials.credentials
    return verify_supabase_jwt(token)