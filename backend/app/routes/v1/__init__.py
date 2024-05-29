from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")


@v1_router.get("/", response_description="Hello, World!", status_code=200)
async def v1_root():
    return {"message": "Hello, World!"}

from .kinde import kinde_router

v1_router.include_router(kinde_router)
