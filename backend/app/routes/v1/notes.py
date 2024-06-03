from fastapi import Depends, Request, APIRouter
from ...database.services import note_service
from ...database import get_session
from .services import user_service

notes_router = APIRouter(prefix="/notes")

@notes_router.post("/add_note")
def add_note(body: note_service.note_schemas.AddNote, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return note_service.add_note(db, body)

@notes_router.post("/move_note")
def move_note(body: note_service.note_schemas.MoveNote, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return note_service.move_note(db, body)

@notes_router.delete("/remove_note")
def remove_note(body: note_service.note_schemas.RemoveNote, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return note_service.remove_note(db, body)

@notes_router.post("/get_notes")
def get_notes(body: note_service.note_schemas.GetNotes, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return note_service.get_notes(db, body)

