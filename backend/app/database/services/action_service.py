from typing import List
from ..models.actions_model import Actions
from ..models.uta_model import UserToAction
from ..models.retros_model import Retros
from .. import Session
from fastapi import HTTPException

async def create_action(db: Session, user_id: str, retro_id: int, name: str, description: str):
    #add permissions checking
    db.add(Actions(retro_id, name, description))

async def asign_users_to_action(db: Session, user_ids: List[str], action_id: int):
    for user_id in user_ids:
        db.add(UserToAction(user_id, action_id))
    
async def remove_users_from_action(db: Session, user_ids: List[str], action_id: int):
    db.query(UserToAction).filter(UserToAction.user_id in user_ids and UserToAction.action_id == action_id).delete()
    
async def remove_action(db: Session, user_id: str, action_id: int):
    #add permissions checking
    db.query(Actions).filter(Actions.action_id == action_id).delete()

async def get_actions_for_group(db: Session, user_id: str, group_id: int):
    return db.query(Actions).filter(Actions.retro_id in retro_service.get_retros_for_org()).all()
    #get actions in a group
    ...
async def get_actions_for_user(db: Session, user_id: str):
    #get actions belonging to a user
    ...