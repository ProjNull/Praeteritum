from fastapi import Depends, Request, APIRouter
from ...database.services import group_service
from ...database import get_session
from .services import user_service


groups_router = APIRouter(prefix="/groups")


@groups_router.post("/invite_user")
async def invite_user(body: group_service.group_schemas.InviteUser, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await group_service.invite_user(db, body, user_id)


@groups_router.post("/join_group")
async def join_group(body: group_service.group_schemas.JoinGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await group_service.join_group(db, body, user_id)

@groups_router.get("/get_invites")
async def get_invites(db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await group_service.get_invites(db, user_id)

@groups_router.delete("/leave_group")
async def leave_group(body: group_service.group_schemas.LeaveGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await group_service.leave_group(db, body, user_id)


@groups_router.post("/create_group")
async def create_group(body: group_service.group_schemas.CreateGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    group = await group_service.create_group(db, body)
    db.commit()
    user_id = kinde_client.get_user_details().get("id")
    await group_service.set_owner(db, group_service.group_schemas.SetOwner(user_id=user_id, group_id=group.group_id))
    return group

@groups_router.post("/update_permissions")
async def update_permissions(body: group_service.group_schemas.UpdatePermissions, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await group_service.update_permissions(db, body, user_id)

@groups_router.delete("/delete_group")
async def delete_group(body: group_service.group_schemas.DeleteGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await group_service.delete_group(db, body, user_id)


@groups_router.post("/get_groups")
async def get_groups(db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await group_service.get_groups(db, user_id)


@groups_router.post("/get_users_in_group")
async def get_users_in_group(body: group_service.group_schemas.GetUsersInGroup, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await group_service.get_users_in_group(db, body, user_id)