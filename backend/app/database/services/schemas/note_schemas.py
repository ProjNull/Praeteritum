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
    retro_id: int
    content: str
    column: int

class MoveNote(BaseModel):
    note_id: int
    column: int

class RemoveNote(BaseModel):
    note_id: int

class GetNotes(BaseModel):
    retro_id: int