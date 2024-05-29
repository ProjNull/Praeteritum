from ..models.notes_model import Notes
from ..models.utr_model import UserToRetro
from ..models.utg_model import UserToGroup
from ..models.retros_model import Retros
from .. import Session
from fastapi import HTTPException

async def create_action(db: Session, user_id: str, retro_id: int):
    #creates an action
    pass
async def remove_action(db: Session, user_id: str, action_id: int):
    #remove an action
    pass
async def get_actions_for_group(db: Session, user_id: str, group_id: int):
    #get actions in a group
    pass
async def get_actions_for_user(db: Session, user_id: str):
    #get actions belonging to a user
    pass