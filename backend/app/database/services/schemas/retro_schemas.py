from pydantic import BaseModel, Field

class RetroBase(BaseModel):
    group_id: int
    name: str
    description: str = Field(default="A retro...")
    columns: list[str]
    display_type: int
    is_public: bool = Field(default=False)

class Retro(RetroBase):
    retro_id: int
    stage: int
    name: str
    description: str
    columns: list[str]
    display_type: int
    is_public: bool
    is_active: bool

class RetroCreate(RetroBase):
    pass

class FilterRetro(BaseModel):
    is_active: bool | None = Field(default=None)
    public_only: bool | None = Field(default=None)

class GetRetro(BaseModel):
    retro_id: int

class GetAllRetrosInGroup(BaseModel):
    group_id: int
    filter: FilterRetro | None

class DeleteRetro(BaseModel):
    retro_id: int

class UpdateRetro(BaseModel):
    retro_id: int
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    is_public: bool | None = Field(default=None)
    stage: int | None = Field(default=None)
    is_active: bool | None = Field(default=None)

class GetRetroMembers(BaseModel):
    retro_id: int

class AddUserToRetro(BaseModel):
    user_id: str
    retro_id: int

class RemoveUserFromRetro(BaseModel):
    user_id: str
    retro_id: int