from typing import List
from ..models.groups_model import Groups
from ..models.retros_model import Retros
from ..models.utg_model import UserToGroup
from ..models.actions_model import Actions
from ..models.uta_model import UserToAction
from .schemas import action_schemas
from .. import Session
from fastapi import HTTPException

async def create_action(db: Session, query: action_schemas.CreateAction, user_id: str):
    group_id: int = db.query(Retros.group_id).filter(Retros.retro_id==query.retro_id).first()
    relation = db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==group_id).first()
    if relation is not None:
        if relation > 1:
            db.add(Actions(query.retro_id, query.name, query.description))
        else:
            raise HTTPException("User is not permited to create an action")
    else:
        raise HTTPException("User is not in this group")

async def asign_users_to_action(db: Session, query: action_schemas.AsignUsersToAction, user_id: str):
    group_id: int = db.query(Retros.group_id).join(Actions, Actions.retro_id == Retros.retro_id).filter(Actions.action_id==query.action_id).first()
    relation = db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==group_id).first()
    if relation is not None:
        if relation > 1:
            for user_id in query.user_ids:
                db.add(UserToAction(user_id, query.action_id))
        else:
            raise HTTPException("User is not permited to asign users to this action")
    else:
        raise HTTPException("User does not have access to this action")

async def remove_users_from_action(db: Session, query: action_schemas.removeUsersFromAction, user_id: str):
    group_id: int = db.query(Retros.group_id).join(Actions, Actions.retro_id == Retros.retro_id).filter(Actions.action_id==query.action_id).first()
    relation =db.query(UserToGroup.permissions).filter(UserToGroup.user_id==user_id, UserToGroup.group_id==group_id).first()
    if relation is not None:
        if relation > 1:
            db.query(UserToAction).filter(UserToAction.user_id in query.user_ids and UserToAction.action_id == query.action_id).delete()
        else:
            raise HTTPException("User is not permited to remove users from this action")
    else:
        raise HTTPException("User does not have access to this action")
        
async def delete_action(db: Session, query: action_schemas.DeleteAction, user_id: str):
    group_id: int = db.query(Retros.group_id).join(Actions, Actions.retro_id == Retros.retro_id).filter(Actions.action_id==query.action_id).first()
    relation =db.query(UserToGroup).filter(UserToGroup.user_id==user_id, UserToGroup.group_id==group_id).first()
    if relation is not None:
        if relation.permissions > 1:
            db.query(Actions).filter(Actions.action_id == query.action_id).delete()
        else:
            raise HTTPException("User is not permited to remove this action")
    else:
        raise HTTPException("User does not have access to this action")

async def get_actions_for_group(db: Session, query: action_schemas.GetActionsForGroup, user_id: str) -> list[Actions]:
    relation = db.query(UserToGroup.utg_id).filter(UserToGroup.user_id==user_id and UserToGroup.group_id==query.group_id).first()
    if relation is not None:
        return db.query(Actions).join(Retros, Actions.retro_id == Retros.retro_id).filter(Retros.group_id == query.group_id)
    else:
        raise HTTPException("User is not in this group")

async def get_actions_for_user(db: Session, user_id: str) -> List[Actions]:
    return db.query(Actions).join(UserToAction, Actions.action_id == UserToAction.action_id).filter(UserToAction.user_id == user_id).all()