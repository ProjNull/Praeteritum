from ..models.example_model import Groups, UserToGroup
from .. import Session

async def example_action(db: Session):
    groups: list[Groups] = db.query(Groups).filter_by(...).all()

async def join_group(db: Session):
    pass
async def leave_group(db: Session):
    pass
async def create_group(db: Session):
    pass
async def delete_group(db: Session):
    pass
async def get_groups(db: Session, user_id):
    pass
async def create_retro(db: Session):
    pass
async def delete_retro(db: Session):
    pass
async def end_retro(db: Session):
    pass
async def get_retros(db: Session, group_id, has_ended: bool):
    pass
async def add_note(db: Session):
    pass
async def move_note(db: Session):
    pass
async def remove_note(db: Session):
    pass
async def get_notes(db: Session, retro_id):
    pass
async def add_vote(db: Session, retro_id, user_id):
    pass
async def get_vote_count(db: Session, retro_id, user_id):
    pass
async def create_action(db: Session):
    pass
async def remove_action(db: Session):
    pass
async def get_actions_for_group(db: Session, group_id):
    pass
async def get_actions_for_user(db: Session, user_id):
    pass