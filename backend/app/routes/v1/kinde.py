from typing import Annotated, Dict

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import RedirectResponse
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import KindeApiClient
from fastapi.security import HTTPBearer

from ...config import (
    GRANT_TYPE,
    KINDE_CLIENT_ID,
    KINDE_CLIENT_SECRET,
    KINDE_HOST,
    KINDE_REDIRECT_URL,
)

configuration = Configuration(host=KINDE_HOST)
kinde_api_client_params = {
    "configuration": configuration,
    "domain": KINDE_HOST,
    "client_id": KINDE_CLIENT_ID,
    "client_secret": KINDE_CLIENT_SECRET,
    "grant_type": GRANT_TYPE,  # client_credentials | authorization_code | authorization_code_with_pkce
    "callback_url": KINDE_REDIRECT_URL,
}

kinde_router = APIRouter(prefix="/kinde")

user_clients: Dict[str, KindeApiClient] = {}


def get_kinde_client(user_id: Annotated[str, Header()]) -> KindeApiClient:
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    if user_id not in user_clients:
        # If the client does not exist, create a new instance with parameters
        user_clients[user_id] = KindeApiClient(**kinde_api_client_params)
    kinde_client = user_clients[user_id]
    # Ensure the client is authenticated
    if not kinde_client.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return kinde_client


@kinde_router.get("/me")
async def me(kinde_client=Depends(get_kinde_client)):
    return kinde_client.get_user_details()


@kinde_router.get("/login")
def login():
    kinde_client = KindeApiClient(**kinde_api_client_params)
    login_url = kinde_client.get_login_url()
    return RedirectResponse(login_url)


# Register endpoint
@kinde_router.get("/register")
def register():
    kinde_client = KindeApiClient(**kinde_api_client_params)
    register_url = kinde_client.get_register_url()
    return RedirectResponse(register_url)


@kinde_router.get("/callback")
def callback(request: Request):
    kinde_client = KindeApiClient(**kinde_api_client_params)
    kinde_client.fetch_token(authorization_response=str(request.url))
    user = kinde_client.get_user_details()
    user_clients[user.get("id")] = kinde_client
    return {"Your id":user.get("id")}


@kinde_router.get("/logout")
def logout(user_id: Annotated[str, Header()]):
    if user_id in user_clients:
        kinde_client = user_clients[user_id]
        logout_url = kinde_client.logout(redirect_to="/api/v1/")
        return RedirectResponse(logout_url)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
    )
