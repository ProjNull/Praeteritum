from ..models.votes_model import Votes
from ..models.utr_model import UserToRetro
from ..models.notes_model import Notes
from .schemas import vote_schemas
from .. import Session
from fastapi import HTTPException

async def add_vote(db: Session, query: vote_schemas.AddVote):
    if db.query(UserToRetro).filter(UserToRetro.user_id==query.user_id and UserToRetro.retro_id == db.query(Notes).filter(Notes.note_id==query.note_id).first().retro_id).first() is not None:
        db.add(Votes(user_id=query.user_id, note_id=query.note_id))
    else:
        raise (HTTPException("User is not a member of this retro"))

async def remove_vote(db: Session, query: vote_schemas.RemoveVote):
    db.query(Votes).filter(Votes.user_id==query.user_id and Votes.note_id==query.note_id).limit(1).delete()

async def get_vote_count(db: Session, query: vote_schemas.GetVoteCount) -> int:
    return db.query(Votes).filter(Votes.user_id == query.user_id and Votes.note_id == db.query(Notes).filter(Notes.retro_id == query.retro_id).first().note_id).count()