from typing import List
from ..models.groups_model import Groups
from ..models.utg_model import UserToGroup
from ..models.invites_model import Invites
from .. import Session
from fastapi import HTTPException

async def invite_user(db: Session, user_id_sender: str, user_id_invited: str, group_id: int):
    if db.query(UserToGroup).filter(UserToGroup.user_id == user_id_sender and UserToGroup.group_id == group_id).first().permissions < 1:
        if db.query(Invites).filter(Invites.user_id == user_id_invited and Invites.group_id == group_id).first() is None:
            if db.query(UserToGroup).filter(UserToGroup.user_id == user_id_invited and UserToGroup.group_id == group_id).first() is None:
                db.add(Invites(user_id=user_id_invited, group_id=group_id))
            else:
                raise (HTTPException("Invited user is already in this group"))
        else:
            raise (HTTPException("Invited user is already invited to this group"))
    else:
        raise (HTTPException("Sender is not permited to invite users to this group"))

async def join_group(db: Session, user_id: str, group_id: int):
    if db.query(Invites).filter(Invites.user_id==user_id and Invites.group_id==group_id).first() is not None:
        db.add(UserToGroup(user_id=user_id, group_id=group_id))
        db.query(Invites).filter(Invites.user_id==user_id and Invites.group_id==group_id).delete()
    else:
        raise (HTTPException("User is not invited to this group"))

async def leave_group(db: Session, user_id: str, group_id: int):
    db.query(UserToGroup).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==group_id).delete()

async def create_group(db: Session, name: str) -> Groups:
    group = Groups(name=name)
    db.add(group)
    return group

async def set_owner(db: Session, user_id: str, group_id: int):
    db.add(UserToGroup(user_id=user_id, group_id=group_id, permissions=4))

async def delete_group(db: Session, user_id:str, group_id: int):
    if db.query(UserToGroup).filter(UserToGroup.user_id==user_id, UserToGroup.group_id==group_id).first().permissions == 4:
        db.query(UserToGroup).filter(UserToGroup.group_id==group_id).delete()
        db.query(Groups).filter(Groups.group_id==group_id).delete()
    else:
        raise (HTTPException("User is not the owner of this group"))
    
async def get_groups(db: Session, user_id: str) -> List[Groups]:
    return db.query(UserToGroup).filter(UserToGroup.user_id==user_id).all()