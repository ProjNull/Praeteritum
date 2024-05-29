from fastapi import Depends, Request, APIRouter
from ...database.services import team_service
from ...database import get_session

teams_router = APIRouter(prefix="/teams")

@teams_router.get("/get_all_teams_in_org")
def get_all_teams_in_org(body: team_service.team_schemas.QueryAllTeamsInOrganization, db = Depends(get_session)):
    return team_service.get_all_teams_in_org(db, body)

@teams_router.get("/get_team_by_id")
def get_team_by_id(body: team_service.team_schemas.QueryTeam, db = Depends(get_session)):
    return team_service.get_team_by_id(db, body)

@teams_router.get("/get_all_team_member_relations")
def get_all_team_member_relations(body: team_service.team_schemas.QueryTeam, db = Depends(get_session)):
    return team_service.get_all_team_member_relations(db, body)

@teams_router.get("/get_team_member_relation_by_id")
def get_team_member_relation_by_idg(body: team_service.team_schemas.QueryTeamMember, db = Depends(get_session)):
    return team_service.get_team_member_relation_by_id(db, body)

@teams_router.get("/get_user_teams")
def get_user_teams(body: team_service.team_schemas.QueryAllUsersTeams, db = Depends(get_session)):
    return team_service.get_user_teams(db, body)

@teams_router.post("/get_user_permission_level_in_team")
def get_user_permission_level_in_team(body: team_service.team_schemas.TeamMember, db = Depends(get_session)):
    return team_service.get_user_permission_level_in_team(db, body)

@teams_router.post("/set_user_permission_level_in_team")
def set_user_permission_level_in_team(body: team_service.team_schemas.TeamMemberUpdate, db = Depends(get_session)):
    return team_service.set_user_permission_level_in_team(db, body)

@teams_router.post("/add_user_to_team")
def add_user_to_team(body: team_service.team_schemas.TeamMemberBase, db = Depends(get_session)):
    return team_service.add_user_to_team(db, body)

@teams_router.post("/remove_user_from_team")
def remove_user_from_team(body: team_service.team_schemas.TeamMemberBase, db = Depends(get_session)):
    return team_service.remove_user_from_team(db, body)

@teams_router.post("/create_team")
def create_team(body: team_service.team_schemas.TeamBase, db = Depends(get_session)):
    return team_service.create_team(db, body)

@teams_router.post("/delete_team")
def delete_team(body: team_service.team_schemas.TeamBase, db = Depends(get_session)):
    return team_service.delete_team(db, body)
