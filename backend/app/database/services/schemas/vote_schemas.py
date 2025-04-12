from pydantic import BaseModel, Field

class AddVote(BaseModel):
    note_id: int

class RemoveVote(BaseModel):
    note_id: int

class GetVoteCount(BaseModel):
    retro_id: int