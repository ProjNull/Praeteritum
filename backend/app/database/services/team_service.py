from typing import List

from .. import Session

from ..models.team_model import TeamModel, TeamPermissionLevel, UserToTeamModel
from .schemas import team_schemas


def get_all_teams_in_org(db: Session, query: team_schemas.QueryAllTeamsInOrganization) -> List[TeamModel]:
    group_id: int = query.organization_id
    return db.query(TeamModel).filter(TeamModel.group_id == group_id).all()


def get_team_by_id(db: Session, query: team_schemas.QueryTeam) -> TeamModel:
    team_id: int = query.team_id
    return db.query(TeamModel).filter(TeamModel.team_id == team_id).first()


def get_all_team_member_relations(db: Session, query: team_schemas.QueryTeam) -> List[UserToTeamModel]:
    team_id: int = query.team_id
    return db.query(UserToTeamModel).filter(UserToTeamModel.team_id == team_id).all()


def get_team_member_relation_by_id(db: Session, query: team_schemas.QueryTeamMember) -> UserToTeamModel:
    user_id: str = query.user_id
    team_id: int = query.team_id
    return db.query(UserToTeamModel).filter(UserToTeamModel.team_id == team_id, UserToTeamModel.user_id == user_id).first()


def get_user_teams(db: Session, query: team_schemas.QueryAllUsersTeams) -> List[TeamModel]:
    user_id: str = query.user_id
    return db.query(TeamModel).join(UserToTeamModel).filter(UserToTeamModel.user_id == user_id.all())
        

def get_user_permission_level_in_team(db: Session, query: team_schemas.QueryTeamMember) -> TeamPermissionLevel:
    team_id: int = query.team_id
    user_id: str = query.user_id
    return get_team_member_relation_by_id(db, team_schemas.QueryTeamMember(team_id=team_id, user_id=user_id)).permission_level


def set_user_permission_level_in_team(db: Session, query: team_schemas.TeamMemberUpdate):
    team_id: int = query.team_id
    user_id: str = query.user_id
    permission_level: int = query.permission_level
    get_team_member_relation_by_id(db, team_schemas.QueryTeamMember(team_id=team_id, user_id=user_id)).set_permission_level(permission_level)


def add_user_to_team(db: Session, query: team_schemas.TeamMemberBase):
    team_id: int = query.team_id
    user_id: str = query.user_id
    db.add(UserToTeamModel(team_id=team_id, user_id=user_id))


def remove_user_from_team(db: Session, query: team_schemas.TeamMemberBase):
    team_id: int = query.team_id
    user_id: str = query.user_id
    get_team_member_relation_by_id(db, team_schemas.QueryTeamMember(team_id=team_id, user_id=user_id)).delete()


def update_team_name(db: Session, query: team_schemas.TeamUpdate):
    team_id: int = query.team_id
    new_name: str = query.name
    
    team = get_team_by_id(db, team_schemas.QueryTeam(team_id=team_id))
    team.name = new_name


def create_team(db: Session, query: team_schemas.TeamBase):
    group_id: int = query.group_id
    name: str = query.name
    
    team: TeamModel = TeamModel(group_id=group_id, name=name)
    db.add(team)


def delete_team(db: Session, query: team_schemas.TeamBase):
    team_id: int = query.team_id
    db.query(UserToTeamModel).filter(UserToTeamModel.team_id == team_id).delete()
    db.query(TeamModel).filter(TeamModel.team_id == team_id).delete()
