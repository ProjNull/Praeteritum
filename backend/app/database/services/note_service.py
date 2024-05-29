from ..models.notes_model import Notes
from ..models.utr_model import UserToRetro
from ..models.utg_model import UserToGroup
from ..models.retros_model import Retros
from .. import Session
from fastapi import HTTPException

async def add_note(db: Session, user_id: str, retro_id: str, content: str, column: int):
    if db.query(UserToRetro).filter(UserToRetro.user_id == user_id and UserToRetro.retro_id == retro_id).first() is not None:
        db.add(Notes(user_id=user_id, retro_id=retro_id, content=content, column=column))
    else:
        raise (HTTPException("User is not a member of this retro"))

async def move_note(db: Session, user_id: str, note_id: int, column: int):
    note = db.query(Notes).filter(Notes.note_id == note_id).first()
    if note.user_id == user_id or db.query(UserToGroup).filter(UserToGroup.user_id == user_id and UserToGroup.group_id == db.query(Retros).filter(Retros.retro_id == note.retro_id).first().group_id).first().permissions > 1:
        note.column = column
        db.add(note)
    else:
        raise (HTTPException("User is not permited to move this note"))

async def remove_note(db: Session, user_id: str, note_id: int):
    note = db.query(Notes).filter(Notes.note_id == note_id).first()
    if note.user_id == user_id or db.query(UserToGroup).filter(UserToGroup.user_id == user_id and UserToGroup.group_id == db.query(Retros).filter(Retros.retro_id == note.retro_id).first().group_id).first().permissions > 1:
        db.query(Notes).filter(Notes.note_id == note_id).delete()
    else:
        raise (HTTPException("User is not permited to remove this note"))

async def get_notes(db: Session, retro_id: int):
    return db.query(Notes).filter(Notes.retro_id == retro_id).all()