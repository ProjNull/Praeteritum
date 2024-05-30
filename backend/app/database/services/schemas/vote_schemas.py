from pydantic import BaseModel, Field

class AddVote(BaseModel):
    user_id: str
    note_id: int

class RemoveVote(BaseModel):
    user_id: str
    note_id: int

class GetVoteCount(BaseModel):
    user_id: str
    retro_id: int