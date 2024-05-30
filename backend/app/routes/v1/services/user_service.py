from datetime import datetime
from typing import Dict, Any

from jose import jwt
from kinde_sdk.kinde_api_client import KindeApiClient

from fastapi import HTTPException, Security, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from kinde_sdk.kinde_api_client import KindeApiClient

from ....config import KINDE_API_CLIENT_PARAMS, KINDE_JWK_KEYS, KINDE_AUDIENCE_API

security = HTTPBearer()

user_clients: Dict[str, KindeApiClient] = {}

def get_login_url() -> str:
    kinde_client = KindeApiClient(**KINDE_API_CLIENT_PARAMS)
    return kinde_client.get_login_url()


def get_register_url() -> str:
    kinde_client = KindeApiClient(**KINDE_API_CLIENT_PARAMS)
    return kinde_client.get_register_url()


def decode_jwt_token(jwt_token: str) -> Dict[str, Any] | None:
    """
    Returns:
        Dict[str, Any] | None: The userid if the token is valid, otherwise None
    """
    if jwt_token is None:
        return None
    for key in KINDE_JWK_KEYS:
        try:
            payload: Dict[str, Any] = jwt.decode(jwt_token, key, algorithms=["RS256"], audience=KINDE_AUDIENCE_API)
            return payload
        except JWTError:
            pass
    return None


def drop_kinde_client(user_id: str):
    if user_id in user_clients:
        user_clients.pop(user_id)


def set_kinde_client(user_id: str, kinde_client: KindeApiClient):
    user_clients[user_id] = kinde_client


def get_kinde_client(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> KindeApiClient:
    payload = decode_jwt_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT Token is Invalid! Please re-log!"
        )
    user_id: str = payload.get("sub", None)
    if user_id not in user_clients or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User state not found! Please re-log!"
        )
    kinde_client = user_clients[user_id]
    if not kinde_client.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Kinde Client isn't Authenticated! Please re-log!"
        )
    return kinde_client
