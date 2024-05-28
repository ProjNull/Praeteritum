from datetime import datetime
from typing import Dict

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from kinde_sdk.kinde_api_client import KindeApiClient

from ....config import JWT_EXPIRE_IN, JWT_SECRET, KINDE_API_CLIENT_PARAMS

security = HTTPBearer()

user_clients: Dict[str, KindeApiClient] = {}

MESSAGE_NOT_AUTHENTICATED: str = "Not authenticated"


def get_login_url() -> str:
    kinde_client = KindeApiClient(**KINDE_API_CLIENT_PARAMS)
    return kinde_client.get_login_url()


def get_register_url() -> str:
    kinde_client = KindeApiClient(**KINDE_API_CLIENT_PARAMS)
    return kinde_client.get_register_url()


def decode_jwt_token(jwt_token: str) -> str | None:
    """
    Returns:
        str | None: The userid if the token is valid, otherwise None
    """
    if jwt_token is None:
        return None
    try:
        payload: Dict[str | None] = jwt.decode(
            jwt_token, JWT_SECRET, algorithms=["HS256"]
        )
        return payload.get("user_id", None)
    except JWTError:
        return None


def create_jwt_token(user_id: str) -> str:
    """
    Creates a JSON Web Token (JWT) for the given user ID.

    Args:
        user_id (str): The kinde user id

    Returns:
        str: The JWT token
    """
    return jwt.encode(
        {"user_id": user_id, "exp": datetime.now() + JWT_EXPIRE_IN},
        JWT_SECRET,
        algorithm="HS256",
    )


def drop_kinde_client(user_id: str):
    if user_id in user_clients:
        user_clients.pop(user_id)


def set_kinde_client(user_id: str, kinde_client: KindeApiClient):
    user_clients[user_id] = kinde_client


def get_kinde_client(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> KindeApiClient:
    user_id = decode_jwt_token(credentials.credentials)
    if user_id not in user_clients or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=MESSAGE_NOT_AUTHENTICATED
        )
    kinde_client = user_clients[user_id]
    if not kinde_client.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=MESSAGE_NOT_AUTHENTICATED
        )
    return kinde_client
