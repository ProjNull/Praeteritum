from typing import List
from ..models.actions_model import Actions
from ..models.uta_model import UserToAction
from .schemas.retro_schemas import QueryAllRetrosInOrganization
from .retro_service import get_all_retros_in_org
from .schemas import action_schemas
from .. import Session
from fastapi import HTTPException

async def create_action(db: Session, query: action_schemas.CreateAction):
    #add permissions checking
    db.add(Actions(query.retro_id, query.name, query.description))

async def asign_users_to_action(db: Session, query: action_schemas.AsignUsersToAction):
    #add permissions checking
    for user_id in query.user_ids:
        db.add(UserToAction(user_id, query.action_id))
    
async def remove_users_from_action(db: Session, query: action_schemas.removeUsersFromAction):
    #add permissions checking
    db.query(UserToAction).filter(UserToAction.user_id in query.user_ids and UserToAction.action_id == query.action_id).delete()
    
async def remove_action(db: Session, query: action_schemas.RemoveAction):
    #add permissions checking
    db.query(Actions).filter(Actions.action_id == query.action_id).delete()

async def get_actions_for_group(db: Session, query: action_schemas.GetActionsForGroup):
    #add permissions checking
    retro_ids = (retro.retro_id for retro in get_all_retros_in_org(db, QueryAllRetrosInOrganization(query.group_id)))
    return db.query(Actions).filter(Actions.retro_id in retro_ids).all()

async def get_actions_for_user(db: Session, query: action_schemas.GetActionsForUser) -> List[Actions]:
    action_ids = (action.action_id for action in db.query(UserToAction).filter(UserToAction.user_id == query.user_id).all())
    return db.query(Actions).filter(Actions.action_id in action_ids).all()