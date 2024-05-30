from pydantic import BaseModel, Field

# class Invite_user(db: Session, user_id_sender: str, user_id_invited: str, group_id: int,
class GroupBase(BaseModel):
    name: str

class Group(GroupBase):
    group_id: int
    name: str

class InviteUser(BaseModel):
    user_id_sender: str
    user_id_invited: str
    group_id: int

class JoinGroup(BaseModel):
    user_id: str
    group_id: int

class LeaveGroup(BaseModel):
    user_id: str
    group_id: int

class CreateGroup(GroupBase):
    name: str

class SetOwner(BaseModel):
    user_id: str
    group_id: int

class DeleteGroup(BaseModel):
    user_id: str
    group_id: int

class GetGroups(BaseModel):
    user_id: str