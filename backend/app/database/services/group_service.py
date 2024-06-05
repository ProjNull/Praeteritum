from typing import List
from ..models.groups_model import Groups
from ..models.utg_model import UserToGroup
from ..models.invites_model import Invites
from .schemas import group_schemas
from .. import Session
from fastapi import HTTPException

async def invite_user(db: Session, query: group_schemas.InviteUser, user_id: str):
    if db.query(UserToGroup).filter(UserToGroup.user_id == user_id and UserToGroup.group_id == query.group_id).first().permissions < 1:
        raise HTTPException("Sender is not permited to invite users to this group")
    
    if db.query(Invites.invite_id).filter(Invites.user_id == query.user_id and Invites.group_id == query.group_id).first() is not None:
        raise HTTPException("Invited user is already invited to this group")
    
    if db.query(UserToGroup.utg_id).filter(UserToGroup.user_id == query.user_id and UserToGroup.group_id == query.group_id).first() is not None:
        raise HTTPException("Invited user is already in this group")
    
    db.add(Invites(user_id=query.user_id, group_id=query.group_id))

async def join_group(db: Session, query: group_schemas.JoinGroup, user_id: str):
    invite_id = db.query(Invites.invite_id).filter(Invites.user_id==user_id and Invites.group_id==query.group_id).first()
    if invite_id is None:
        raise HTTPException("User is not invited to this group")
    
    db.add(UserToGroup(user_id=user_id, group_id=query.group_id))
    db.query(Invites).filter(Invites.invite_id==invite_id).delete()

async def leave_group(db: Session, query: group_schemas.LeaveGroup, user_id: str):
    relation = db.query(UserToGroup).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==query.group_id).first()
    if relation.permissions == 4:
        raise HTTPException("User is owner of this group, so you can't leave this group, you must transfer ownership or delete it instead")
    
    db.query(UserToGroup).filter(UserToGroup.utg_id==relation.utg_id).delete()

async def remove_from_group(db: Session, query: group_schemas.RemoveFromGroup, user_id: str):
    relation = db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==query.group_id).first()
    if relation is None:
        raise HTTPException("User is not in this group")
    
    relation2 = db.query(UserToGroup).filter(UserToGroup.user_id==query.user_id and UserToGroup.group_id==query.group_id).first()
    if relation2 is None:
        raise HTTPException("User to be kicked is not in this group")
    
    if relation < relation2.permissions:
        raise HTTPException("User is not permited to remove this user from this group")
    
    db.query(UserToGroup).filter(UserToGroup.utg_id==relation2.utg_id).delete()
    
async def create_group(db: Session, query: group_schemas.CreateGroup) -> Groups:
    group = Groups(name=query.name)
    db.add(group)
    return group

async def set_owner(db: Session, query: group_schemas.SetOwner):
    db.add(UserToGroup(user_id=query.user_id, group_id=query.group_id, permissions=4))

async def delete_group(db: Session, query: group_schemas.DeleteGroup, user_id: str):
    if db.query(UserToGroup).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==query.group_id).first().permissions != 4:
        raise (HTTPException("User is not the owner of this group"))
    
    db.query(UserToGroup).filter(UserToGroup.group_id==query.group_id).delete()
    db.query(Groups).filter(Groups.group_id==query.group_id).delete()
    
async def get_groups(db: Session, user_id: str) -> List[Groups]:
    return db.query(Groups).join(UserToGroup, Groups.group_id == UserToGroup.group_id) .filter(UserToGroup.user_id==user_id).all()

async def get_users_in_group(db: Session, query: group_schemas.GetUsersInGroup, user_id: str) -> List[str]:
    if db.query(UserToGroup.user_id).filter(UserToGroup.group_id==query.group_id and UserToGroup.user_id==user_id).first() is None:
        raise HTTPException("User does not have access to this group")
    
    return [id.user_id for id in db.query(UserToGroup).filter(UserToGroup.group_id==query.group_id).all()]