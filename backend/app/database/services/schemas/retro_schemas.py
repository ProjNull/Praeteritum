from pydantic import BaseModel, Field


class RetroBase(BaseModel):
    organization_id: int
    name: str
    description: str = Field(default="A retro...")
    is_public: bool = Field(default=False)


class RetroCreate(RetroBase):
    pass


class RetroUpdate(BaseModel):
    stage: int | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    is_public: bool | None = Field(default=None)


class Retro(RetroBase):
    retro_id: int
    stage: int
    is_active: bool
    name: str
    description: str
    is_public: bool

class QueryAllRetrosInOrganization(BaseModel):
    organization_id: int

class QueryRetro(RetroBase):
    retro_id: int

class QueryAllRetrosForUser(BaseModel):
    user_id: str

class QueryRetroList(BaseModel):
    organization_id: int
    match_active: bool = Field(default=False, description="If true, the retro's is_active must match with the required is_active state, otherwise the param is ignored")
    is_active: bool = Field(default=True)
    public_only: bool = Field(default=False)

class UserToRetro(BaseModel):
    user_id: str
    retro_id: int
