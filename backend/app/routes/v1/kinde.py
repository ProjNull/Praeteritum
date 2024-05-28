from typing import Union
from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import KindeApiClient, GrantType
import config

kinde_router = APIRouter(prefix="/kinde")

kinde_router.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

# User clients dictionary to store Kinde clients for each user
user_clients = {}

# Initialize Kinde client with configuration
configuration = Configuration(host=config.KINDE_ISSUER_URL)
kinde_api_client_params = {
    "configuration": configuration,
    "domain": config.KINDE_ISSUER_URL,
    "client_id": config.CLIENT_ID,
    "client_secret": config.CLIENT_SECRET,
    "grant_type": config.GRANT_TYPE,
    "callback_url": config.KINDE_CALLBACK_URL,
}
if config.GRANT_TYPE == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
    kinde_api_client_params["code_verifier"] = config.CODE_VERIFIER

# User clients dictionary to store Kinde clients for each user
user_clients = {}

# Dependency to get the current user's KindeApiClient instance
def get_kinde_client(request: Request) -> KindeApiClient:
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if user_id not in user_clients:
        # If the client does not exist, create a new instance with parameters
        user_clients[user_id] = KindeApiClient(**kinde_api_client_params)

    kinde_client = user_clients[user_id]
    # Ensure the client is authenticated
    if not kinde_client.is_authenticated():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return kinde_client

# Login endpoint
@kinde_router.get("/api/auth/login")
def login(request: Request):
    kinde_client = KindeApiClient(**kinde_api_client_params)
    login_url = kinde_client.get_login_url()
    return RedirectResponse(login_url)

# Register endpoint
@kinde_router.get("/api/auth/register")
def register(request: Request):
    kinde_client = KindeApiClient(**kinde_api_client_params)
    register_url = kinde_client.get_register_url()
    return RedirectResponse(register_url)

@kinde_router.get("/api/auth/kinde_callback")
def callback(request: Request):
    kinde_client = KindeApiClient(**kinde_api_client_params)
    kinde_client.fetch_token(authorization_response=str(request.url))
    user = kinde_client.get_user_details()
    request.session["user_id"] = user.get("id")
    user_clients[user.get("id")] = kinde_client
    return RedirectResponse(kinde_router.url_path_for("read_root"))

# Logout endpoint
@kinde_router.get("/api/auth/logout")
def logout(request: Request):
    user_id = request.session.get("user_id")
    if user_id in user_clients:
        kinde_client = user_clients[user_id]
        logout_url = kinde_client.logout(redirect_to=config.LOGOUT_REDIRECT_URL)
        del user_clients[user_id]
        request.session.pop("user_id", None)
        return RedirectResponse(logout_url)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")