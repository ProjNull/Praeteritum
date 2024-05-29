from ..models.example_model import Groups, UserToGroup
from .. import Session

async def example_action(db: Session):
    groups: list[Groups] = db.query(Groups).filter_by(...).all()

async def join_group(db: Session, user_id: str, group_id: int):
    #implement check if has invite
    pass
async def leave_group(db: Session, user_id: str, group_id: int):
    pass
async def create_group(db: Session, user_id: str, name: str):
    #create a group and add a utg relation, with highest permissions
    pass
async def delete_group(db: Session, user_id:str, group_id: int):
    #check permissions, delete all utg relations
    pass
async def get_groups(db: Session, user_id: str):
    #return all groups
    pass
async def create_retro(db: Session, user_id: str, group_id: int):
    #create a retro
    pass
async def delete_retro(db: Session, user_id: str, retro_id: int):
    #remove a retro
    pass
async def end_retro(db: Session, user_id: str, retro_id: int):
    #end retro (close it)
    pass
async def get_retros(db: Session, user_id: str, group_id: int, has_ended: bool):
    #get all retros in a group
    pass
async def add_note(db: Session, user_id: str, retro_id: str):
    #add a note to retro
    pass
async def move_note(db: Session, user_id: str, note_id: int):
    #move note (permissions)
    pass
async def remove_note(db: Session, user_id: str, note_id: int):
    #remove note (permissions)
    pass
async def get_notes(db: Session, retro_id: int):
    #get notes
    pass
async def add_vote(db: Session, retro_id: int, user_id: str):
    #add a vote
    pass
async def get_vote_count(db: Session, user_id: str, retro_id: int):
    #return the number of votes in a retro
    pass
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