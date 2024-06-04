from typing import List
from ..models.groups_model import Groups
from ..models.utg_model import UserToGroup
from ..models.invites_model import Invites
from .schemas import group_schemas
from .. import Session
from fastapi import HTTPException

async def invite_user(db: Session, query: group_schemas.InviteUser, user_id: str):
    if db.query(UserToGroup.permissions).filter(UserToGroup.user_id == user_id and UserToGroup.group_id == query.group_id).first() < 1:
        if db.query(Invites.invite_id).filter(Invites.user_id == query.user_id and Invites.group_id == query.group_id).first() is None:
            if db.query(UserToGroup.utg_id).filter(UserToGroup.user_id == query.user_id and UserToGroup.group_id == query.group_id).first() is None:
                db.add(Invites(user_id=query.user_id, group_id=query.group_id))
            else:
                raise HTTPException("Invited user is already in this group")
        else:
            raise HTTPException("Invited user is already invited to this group")
    else:
        raise HTTPException("Sender is not permited to invite users to this group")

async def join_group(db: Session, query: group_schemas.JoinGroup, user_id: str):
    invite_id = db.query(Invites.invite_id).filter(Invites.user_id==user_id and Invites.group_id==query.group_id).first()
    if invite_id is not None:
        db.add(UserToGroup(user_id=user_id, group_id=query.group_id))
        db.query(Invites).filter(Invites.invite_id==invite_id).delete()
    else:
        raise HTTPException("User is not invited to this group")

async def leave_group(db: Session, query: group_schemas.LeaveGroup, user_id: str):
    relation = db.query(UserToGroup).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==query.group_id).first()
    if relation.permissions != 4:
        db.query(UserToGroup).filter(UserToGroup.utg_id==relation.utg_id).delete()
    else:
        raise HTTPException("User is owner of this group, so you can't leave this group, you must transfer ownership or delete it instead")

async def remove_from_group(db: Session, query: group_schemas.RemoveFromGroup, user_id: str):
    relation = db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==query.group_id).first()
    if relation is not None:
        relation2 = db.query(UserToGroup).filter(UserToGroup.user_id==query.user_id and UserToGroup.group_id==query.group_id).first()
        if relation2 is not None:
            if relation > relation2.permissions:
                db.query(UserToGroup).filter(UserToGroup.utg_id==relation2.utg_id).delete()
            else:
                raise HTTPException("User is not permited to remove this user from this group")
        else:
            raise HTTPException("User to be kicked is not in this group")
    else:
        raise HTTPException("User is not in this group")
    
async def create_group(db: Session, query: group_schemas.CreateGroup) -> Groups:
    group = Groups(name=query.name)
    db.add(group)
    return group

async def set_owner(db: Session, query: group_schemas.SetOwner):
    db.add(UserToGroup(user_id=query.user_id, group_id=query.group_id, permissions=4))

async def delete_group(db: Session, query: group_schemas.DeleteGroup, user_id: str):
    if db.query(UserToGroup).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==query.group_id).first().permissions == 4:
        db.query(UserToGroup).filter(UserToGroup.group_id==query.group_id).delete()
        db.query(Groups).filter(Groups.group_id==query.group_id).delete()
    else:
        raise (HTTPException("User is not the owner of this group"))
    
async def get_groups(db: Session, user_id: str) -> List[Groups]:
    return db.query(Groups).join(UserToGroup, Groups.group_id == UserToGroup.group_id) .filter(UserToGroup.user_id==user_id).all()

async def get_users_in_group(db: Session, query: group_schemas.GetUsersInGroup, user_id: str) -> List[str]:
    if db.query(UserToGroup.user_id).filter(UserToGroup.group_id==query.group_id, UserToGroup.user_id==user_id).first() is not None:
        return db.query(UserToGroup.user_id).filter(UserToGroup.group_id==query.group_id).all()
    else:
        raise HTTPException("User does not have access to this group")