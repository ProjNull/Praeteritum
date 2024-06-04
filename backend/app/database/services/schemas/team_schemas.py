from pydantic import BaseModel, Field

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    organization_id: int

class TeamUpdate(TeamBase):
    pass

class Team(TeamBase):
    team_id: int
    organization_id: int

    class Config:
        orm_mode = True

class TeamMemberBase(BaseModel):
    team_id: int
    user_id: str

class TeamMemberUpdate(TeamMemberBase):
    permission_level: int = Field(default=1)

class TeamMemberCreate(TeamMemberUpdate):
    pass

class TeamMember(TeamMemberBase):
    utt_id: int
    permission_level: int

    class Config:
        orm_mode = True

class QueryAllTeamsInOrganization(BaseModel):
    organization_id: int

class QueryTeam(BaseModel):
    team_id: int

class QueryAllUsersTeams(BaseModel):
    user_id: str

class QueryMembersInTeam(QueryTeam):
    team_id: int

class QueryTeamMember(TeamMemberBase):
    pass
