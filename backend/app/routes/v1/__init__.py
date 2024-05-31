from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")


@v1_router.get("/", response_description="Hello, World!", status_code=200)
async def v1_root():
    return {"message": "Hello, World!"}

from .kinde import kinde_router
from .groups import groups_router
from .teams import teams_router
from .retrospectives import retrospectives_router
from .notes import notes_router

v1_router.include_router(kinde_router)
v1_router.include_router(groups_router)
v1_router.include_router(teams_router)
v1_router.include_router(retrospectives_router)
v1_router.include_router(notes_router)