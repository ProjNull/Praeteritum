from ..models.votes_model import Votes
from ..models.utr_model import UserToRetro
from ..models.utg_model import UserToGroup
from ..models.retros_model import Retros
from .. import Session
from fastapi import HTTPException

async def add_vote(db: Session, retro_id: int, user_id: str):
    db.add(Votes(retro_id=retro_id, note_id=))
async def get_vote_count(db: Session, user_id: str, retro_id: int):
    #return the number of votes in a retro
    pass