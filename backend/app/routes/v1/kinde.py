from typing import Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from kinde_sdk.kinde_api_client import KindeApiClient

from ...config import KINDE_API_CLIENT_PARAMS
from .services import user_service

kinde_router = APIRouter(prefix="/kinde")


@kinde_router.get("/me")
async def me(kinde_client=Depends(user_service.get_kinde_client)):
    return kinde_client.get_user_details()


@kinde_router.get("/login")
def login():
    return RedirectResponse(user_service.get_login_url())


@kinde_router.get("/register")
def register():
    return RedirectResponse(user_service.get_register_url())


@kinde_router.get("/callback")
def callback(request: Request):
    kinde_client = KindeApiClient(**KINDE_API_CLIENT_PARAMS)
    kinde_client.fetch_token(authorization_response=str(request.url))
    user = kinde_client.get_user_details()
    user_service.set_kinde_client(user.get("id"), kinde_client)
    # TODO: Wtf
    return RedirectResponse("http://localhost:3000/")


@kinde_router.get("/logout")
def logout(kinde_client: KindeApiClient = Depends(user_service.get_kinde_client)):
    logout_url = kinde_client.logout(redirect_to="/")
    user_service.drop_kinde_client(kinde_client.get_user_details().get("id"))
    return RedirectResponse(logout_url, headers={"Authorization": f"Bearer {kinde_client.configuration.access_token}"})


@kinde_router.get("/token")
def token(payload: Dict = Depends(user_service.get_token_payload)):
    kinde_client: KindeApiClient | None = user_service.user_clients.get(payload.get("sub"), None)
    if kinde_client is None:
        return RedirectResponse("/api/v1/kinde/login")
    return {"token": kinde_client.configuration.access_token}
