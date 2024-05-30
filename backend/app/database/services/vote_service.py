from ..models.votes_model import Votes
from ..models.utr_model import UserToRetro
from ..models.notes_model import Notes
from .. import Session
from fastapi import HTTPException

async def add_vote(db: Session, user_id: str, note_id: int):
    """
    Adds a vote for a user to a note.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user.
        note_id (int): The ID of the note.

    Raises:
        HTTPException: If the user is not a member of the retro associated with the note.

    Returns:
        None
    """
    if db.query(UserToRetro).filter(UserToRetro.user_id==user_id and UserToRetro.retro_id == db.query(Notes).filter(Notes.note_id==note_id).first().retro_id).first() is not None:
        db.add(Votes(user_id=user_id, note_id=note_id))
    else:
        raise (HTTPException("User is not a member of this retro"))

async def get_vote_count(db: Session, user_id: str, retro_id: int) -> int:
    """
    Retrieves the count of votes for a specific user in a retro.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user.
        retro_id (int): The ID of the retro.

    Returns:
        int
    """
    return db.query(Votes).filter(Votes.user_id == user_id and Votes.note_id == db.query(Notes).filter(Notes.retro_id == retro_id).first().note_id).count()