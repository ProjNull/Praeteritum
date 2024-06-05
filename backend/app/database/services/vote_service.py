from ..models.votes_model import Votes
from ..models.utr_model import UserToRetro
from ..models.notes_model import Notes
from .schemas import vote_schemas
from .. import Session
from fastapi import HTTPException, status

async def add_vote(db: Session, query: vote_schemas.AddVote):
    is_member = db.query(UserToRetro).filter(
        UserToRetro.user_id==query.user_id and 
        UserToRetro.retro_id==db.query(Notes).filter(
            Notes.note_id==query.note_id).first().retro_id).first() # Noone is gonna read this anyway

    if is_member is None: raise HTTPException(detail="User is not a member of this retro", status_code=status.HTTP_403_FORBIDDEN)
    db.add(Votes(user_id=query.user_id, note_id=query.note_id))

async def remove_vote(db: Session, query: vote_schemas.RemoveVote, user_id: str):
    db.query(Votes).filter(Votes.user_id==user_id and Votes.note_id==query.note_id).limit(1).delete()

async def get_vote_count(db: Session, query: vote_schemas.GetVoteCount, user_id: str) -> int:
    return db.query(Votes).join(Notes, Votes.note_id == Notes.note_id).filter(Votes.user_id == user_id and Notes.retro_id == query.retro_id).count()

 