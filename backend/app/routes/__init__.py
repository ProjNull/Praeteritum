from fastapi import APIRouter

api_router = APIRouter(prefix="/api")

from .v1 import v1_router

api_router.include_router(v1_router)
