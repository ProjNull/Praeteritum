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


# Register endpoint
@kinde_router.get("/register")
def register():
    kinde_client = KindeApiClient(**KINDE_API_CLIENT_PARAMS)
    register_url = kinde_client.get_register_url()
    return RedirectResponse(register_url)


@kinde_router.get("/callback")
def callback(request: Request):
    kinde_client = KindeApiClient(**KINDE_API_CLIENT_PARAMS)
    kinde_client.fetch_token(authorization_response=str(request.url))
    user = kinde_client.get_user_details()
    user_service.set_kinde_client(user.get("id"), kinde_client)
    return {"user_id": user.get("id"), "token": user_service.create_jwt_token(user.get("id"))}


@kinde_router.get("/logout")
def logout(kinde_client: KindeApiClient = Depends(user_service.get_kinde_client)):
    logout_url = kinde_client.logout(redirect_to="/api/v1/")
    user_service.drop_kinde_client(kinde_client.user_id)
    return RedirectResponse(logout_url)
