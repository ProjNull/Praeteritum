from ..models.notes_model import Notes
from ..models.utr_model import UserToRetro
from ..models.utg_model import UserToGroup
from ..models.retros_model import Retros
from .schemas import note_schemas
from .. import Session
from fastapi import HTTPException, status

async def add_note(db: Session, query: note_schemas.AddNote, user_id: str):
    is_member = db.query(UserToRetro.utr_id).filter(UserToRetro.user_id == user_id and UserToRetro.retro_id == query.retro_id).first()
    
    # Not a member
    if is_member is None: raise (HTTPException(detail="User is not a member of this retro", status_code=status.HTTP_403_FORBIDDEN))
        
    db.add(Notes(user_id=user_id, retro_id=query.retro_id, content=query.content, column=query.column))
    

async def move_note(db: Session, query: note_schemas.MoveNote, user_id: str):
    note = db.query(Notes).filter(Notes.note_id == query.note_id).first()
    group_id = db.query(Retros).filter(Retros.retro_id == note.retro_id).first().group_id
    is_permitted = note.user_id == user_id or db.query(UserToGroup).filter(UserToGroup.user_id == user_id and UserToGroup.group_id == group_id).first().permissions
    
    # Is permitted 
    if is_permitted > 1: raise (HTTPException(detail="User is not permited to move this note", status_code=status.HTTP_403_FORBIDDEN))
    note.column = query.column
    db.add(note)


async def remove_note(db: Session, query: note_schemas.RemoveNote, user_id: str):
    note = db.query(Notes).filter(Notes.note_id == query.note_id).first()
    is_permitted = note.user_id == user_id or db.query(UserToGroup).filter(UserToGroup.user_id == user_id and UserToGroup.group_id == db.query(Retros).filter(Retros.retro_id == note.retro_id).first().group_id).first().permissions
    
    # Is permitted
    if is_permitted > 1: raise (HTTPException(detail="User is not permited to remove this note", status_code=status.HTTP_403_FORBIDDEN))

    db.query(Notes).filter(Notes.note_id == query.note_id).delete()
        

async def get_notes(db: Session, query: note_schemas.GetNotes, user_id: str):
    is_member = db.query(UserToRetro.utr_id).filter(UserToRetro.user_id == user_id and UserToRetro.retro_id == query.retro_id).first()
    
    # is_member
    if is_member is None: raise (HTTPException(detail="User is not a member of this retro", status_code=status.HTTP_403_FORBIDDEN))
    
    return db.query(Notes).filter(Notes.retro_id == query.retro_id).all()