from typing import List
from pydantic import BaseModel, Field

class ActionBase(BaseModel):
    retro_id: int
    name: str
    description: str = Field(default="An action...")

class Action(ActionBase):
    action_id: int
    retro_id: int
    name: str
    description: str

class CreateAction(BaseModel):
    retro_id: int
    name: str
    description: str

class AsignUsersToAction(BaseModel):
    user_ids: List[str]
    action_id: int

class removeUsersFromAction(BaseModel):
    user_ids: List[str]
    action_id: int

class DeleteAction(BaseModel):
    action_id: int

class GetActionsForGroup(BaseModel):
    group_id: int