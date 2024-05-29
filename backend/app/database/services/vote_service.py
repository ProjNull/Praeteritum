from ..models.votes_model import Votes
from ..models.utr_model import UserToRetro
from ..models.notes_model import Notes
from .. import Session
from fastapi import HTTPException

async def add_vote(db: Session, user_id: str, note_id: int):
    if db.query(UserToRetro).filter(UserToRetro.user_id==user_id and UserToRetro.retro_id == db.query(Notes).filter(Notes.note_id==note_id).first().retro_id).first() is not None:
        db.add(Votes(user_id=user_id, note_id=note_id))
    else:
        raise (HTTPException("User is not a member of this retro"))

async def get_vote_count(db: Session, user_id: str):
    
    #return the number of votes in a retro
    ...