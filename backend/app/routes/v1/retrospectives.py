from fastapi import Depends, Request, APIRouter
from ...database.services import retro_service
from ...database import get_session
from .services import user_service

retrospectives_router = APIRouter(prefix="/retrospectives")

@retrospectives_router.post("/create_retro")
async def create_retro(body: retro_service.retro_schemas.RetroCreate, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await retro_service.create_retro(db, body, user_id)

@retrospectives_router.post("/get_retro_by_id")
async def get_retro_by_id(body: retro_service.retro_schemas.GetRetro, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await retro_service.get_retro_by_id(db, body, user_id)

@retrospectives_router.post("/get_all_retros_in_group")
async def get_all_retros_in_org(body: retro_service.retro_schemas.GetAllRetrosInGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await retro_service.get_all_retros_in_group(db, body, user_id)

@retrospectives_router.post("/get_all_retros_by_user")
async def get_all_retros_by_user(body: retro_service.retro_schemas.FilterRetro, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await retro_service.get_all_retros_for_user(db, body, user_id)

@retrospectives_router.delete("/delete_retro")
async def delete_retro(body: retro_service.retro_schemas.DeleteRetro, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await retro_service.delete_retro(db, body, user_id)

@retrospectives_router.patch("/update_retro")
async def update_retro(body: retro_service.retro_schemas.UpdateRetro, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await retro_service.update_retro(db, body, user_id)

@retrospectives_router.post("/get_retro_members")
async def get_retro_members(body: retro_service.retro_schemas.QueryRetro, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await retro_service.get_retro_members(db, body, user_id)

@retrospectives_router.post("/add_user_to_retro")
async def add_user_to_retro(body: retro_service.retro_schemas.UserToRetro, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await retro_service.add_user_to_retro(db, body, user_id)

@retrospectives_router.delete("/remove_user_from_retro")
async def remove_user_from_retro(body: retro_service.retro_schemas.UserToRetro, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await retro_service.remove_user_from_retro(db, body, user_id)
