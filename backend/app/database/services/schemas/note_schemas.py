from pydantic import BaseModel, Field

class NoteBase(BaseModel):
    user_id: str
    retro_id: int
    content: str
    column: int

class Note(NoteBase):
    note_id: int
    user_id: str
    retro_id: int
    content: str
    column: int

class AddNote(BaseModel):
    user_id: str
    retro_id: str
    content: str
    column: int

class MoveNote(BaseModel):
    user_id: str
    note_id: int
    column: int

class RemoveNote(BaseModel):
    user_id: str
    note_id: int

class GetNotes(BaseModel):
    retro_id: int