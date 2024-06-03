from fastapi import Depends, Request, APIRouter
from ...database.services import action_service
from ...database import get_session
from .services import user_service

actions_router = APIRouter(prefix="/actions")

@actions_router.post("/create_retro")
async def create_action(body: action_service.action_schemas.CreateAction, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return await action_service.create_action(db, body)

@actions_router.post("/asign_users_to_action")
async def asign_users_to_action(body: action_service.action_schemas.AsignUsersToAction, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return await action_service.asign_users_to_action(db, body)

@actions_router.post("/remove_users_from_action")
async def remove_users_from_action(body: action_service.action_schemas.removeUsersFromAction, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return await action_service.remove_users_from_action(db, body)

@actions_router.post("/delete_action")
async def delete_action(body: action_service.action_schemas.DeleteAction, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return await action_service.delete_action(db, body)

@actions_router.post("/get_actions_for_group")
async def get_actions_for_group(body: action_service.action_schemas.GetActionsForGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return await action_service.get_actions_for_group(db, body)

@actions_router.post("/get_actions_for_user")
async def get_actions_for_user(body: action_service.action_schemas.GetActionsForUser, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return await action_service.get_actions_for_user(db, body)
