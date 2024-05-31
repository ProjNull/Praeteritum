from fastapi import Depends, Request, APIRouter
from ...database.services import group_service
from ...database import get_session
from .services import user_service

groups_router = APIRouter(prefix="/groups")

@groups_router.post("/invite_user")
def invite_user(body: group_service.group_schemas.InviteUser, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return group_service.invite_user(db, body)

@groups_router.get("/join_group")
def join_group(body: group_service.group_schemas.JoinGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return group_service.join_group(db, body)

@groups_router.delete("/leave_group")
def leave_group(body: group_service.group_schemas.LeaveGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return group_service.leave_group(db, body)

@groups_router.post("/create_group")
def create_group(body: group_service.group_schemas.CreateGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return group_service.create_group(db, body)

@groups_router.patch("/set_owner")
def set_owner(body: group_service.group_schemas.SetOwner, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return group_service.set_owner(db, body)

@groups_router.delete("/delete_group")
def delete_group(body: group_service.group_schemas.DeleteGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return group_service.delete_group(db, body)

@groups_router.get("/get_groups")
def get_groups(body: group_service.group_schemas.GetGroups, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return group_service.get_groups(db, body)
