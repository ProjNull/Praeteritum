from pydantic import BaseModel, Field

class GroupBase(BaseModel):
    name: str

class Group(GroupBase):
    group_id: int
    name: str

class InviteUser(BaseModel):
    user_id: str
    group_id: int

class JoinGroup(BaseModel):
    group_id: int

class LeaveGroup(BaseModel):
    group_id: int

class RemoveFromGroup(BaseModel):
    user_id: str
    group_id: int

class CreateGroup(GroupBase):
    name: str

class SetOwner(BaseModel):
    user_id: str
    group_id: int

class DeleteGroup(BaseModel):
    group_id: int

class GetGroups(BaseModel):
    user_id: str

class GetUsersInGroup(BaseModel):
    group_id: int