import os
from datetime import timedelta
from typing import Dict, List
import secrets

import dotenv
import jose
import jose.jwk
import requests
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType

dotenv.load_dotenv()

# Databases
DB_DRIVER: str = os.environ.get("DB_DRIVER", "postgresql")
DB_HOST: str = os.environ.get("DB_HOST", "postgres")
DB_PORT: str = os.environ.get("DB_PORT", "5432")
DB_USER: str = os.environ.get("DB_USER", "prae")
DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "password")
DB_NAME: str = os.environ.get("DB_NAME", "prae")
CACHE_HOST: str = os.environ.get("CACHE_HOST", "redis")
CACHE_PORT: str = os.environ.get("CACHE_PORT", "6379")

# Kinde
KINDE_CLIENT_ID: str = os.environ.get("KINDE_CLIENT_ID", None)
KINDE_CLIENT_SECRET: str = os.environ.get("KINDE_CLIENT_SECRET", None)
KINDE_HOST: str = os.environ.get("KINDE_HOST", None)
KINDE_REDIRECT_URL: str = os.environ.get("KINDE_REDIRECT_URL", None)

if not all([KINDE_CLIENT_ID, KINDE_CLIENT_SECRET, KINDE_HOST, KINDE_REDIRECT_URL]):
    raise ValueError(
        "Improper KINDE configuration has been provided, please make sure all of the following variables are set: KINDE_CLIENT_ID, KINDE_CLIENT_SECRET, KINDE_HOST, KINDE_REDIRECT_URL"
    )

GRANT_TYPE: GrantType = "authorization_code"
match (os.environ.get("GRANT_TYPE", "client_credentials").lower()):
    case "client_credentials":
        GRANT_TYPE = GrantType.CLIENT_CREDENTIALS
    case "authorization_code":
        GRANT_TYPE = GrantType.AUTHORIZATION_CODE
    case "authorization_code_with_pkce":
        GRANT_TYPE = GrantType.AUTHORIZATION_CODE_WITH_PKCE

configuration = Configuration(host=KINDE_HOST)
KINDE_API_CLIENT_PARAMS: Dict = {
    "configuration": configuration,
    "domain": KINDE_HOST,
    "client_id": KINDE_CLIENT_ID,
    "client_secret": KINDE_CLIENT_SECRET,
    "grant_type": GRANT_TYPE,  # client_credentials | authorization_code | authorization_code_with_pkce
    "callback_url": KINDE_REDIRECT_URL,
    "audience": "127.0.0.1",
}

KINDE_AUDIENCE_API: str = os.environ.get("KINDE_AUDIENCE_API", "127.0.0.1")
if KINDE_AUDIENCE_API != "127.0.0.1":
    KINDE_API_CLIENT_PARAMS["audience"] = KINDE_AUDIENCE_API
else:
    print(
        "Audience is set as 127.0.0.1, this will not work in a production environment"
    )

# JWT

# DEPRECATED: We no longer use our own JWTs, instead we use the ones supplied by Kinde
JWT_SECRET: str = os.environ.get("JWT_SECRET", secrets.token_hex(32))
try:
    # DEPRECATED: We no longer use our own JWTs, instead we use the ones supplied by Kinde
    JWT_EXPIRE_IN: timedelta = timedelta(
        seconds=int(os.environ.get("JWT_EXPIRE_IN", "86400"))
    )
except ValueError:
    # DEPRECATED: We no longer use our own JWTs, instead we use the ones supplied by Kinde
    JWT_EXPIRE_IN: timedelta = timedelta(seconds=86400)


def load_jwks(jwk_url: str) -> List[jose.jwk.Key]:
    try:
        response = requests.get(jwk_url)
    except Exception as e:
        raise RuntimeError(
            "Could not download JWKs from remote (" + jwk_url + ")"
        ) from e
    jwk_set = response.json()
    keys = jwk_set.get("keys", [])
    key_objects = []
    errors = 0
    for key in keys:
        try:
            jwk = jose.jwk.construct(key)
        except jose.exceptions.JWKError:
            errors += 1
            continue
        key_objects.append(jwk)
        print(
            f"Loaded {len(key_objects)} JWKs ({errors} errors) from remote " + jwk_url
        )
    return key_objects


KINDE_JWK_KEYS: List[jose.jwk.Key] = load_jwks(KINDE_HOST + "/.well-known/jwks.json")
