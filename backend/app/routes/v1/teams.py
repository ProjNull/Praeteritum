from fastapi import Depends, Request, APIRouter
from ...database.services import team_service
from ...database import get_session
from .services import user_service

teams_router = APIRouter(prefix="/teams")

@teams_router.post("/get_all_teams_in_org")
async def get_all_teams_in_org(body: team_service.team_schemas.QueryAllTeamsInOrganization, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.get_all_teams_in_org(db, body)

@teams_router.post("/get_team_by_id")
async def get_team_by_id(body: team_service.team_schemas.QueryTeam, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.get_team_by_id(db, body)

@teams_router.post("/get_all_team_member_relations")
async def get_all_team_member_relations(body: team_service.team_schemas.QueryTeam, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.get_all_team_member_relations(db, body)

@teams_router.post("/get_team_member_relation_by_id")
async def get_team_member_relation_by_idg(body: team_service.team_schemas.QueryTeamMember, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.get_team_member_relation_by_id(db, body)

@teams_router.post("/get_user_teams")
async def get_user_teams(body: team_service.team_schemas.QueryAllUsersTeams, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.get_user_teams(db, body)

@teams_router.post("/get_user_permission_level_in_team")
async def get_user_permission_level_in_team(body: team_service.team_schemas.TeamMember, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.get_user_permission_level_in_team(db, body)

@teams_router.post("/set_user_permission_level_in_team")
async def set_user_permission_level_in_team(body: team_service.team_schemas.TeamMemberUpdate, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.set_user_permission_level_in_team(db, body)

@teams_router.post("/add_user_to_team")
async def add_user_to_team(body: team_service.team_schemas.TeamMemberBase, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.add_user_to_team(db, body)

@teams_router.post("/remove_user_from_team")
async def remove_user_from_team(body: team_service.team_schemas.TeamMemberBase, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.remove_user_from_team(db, body)

@teams_router.post("/create_team")
async def create_team(body: team_service.team_schemas.TeamCreate, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.create_team(db, body)

@teams_router.delete("/delete_team")
async def delete_team(body: team_service.team_schemas.TeamBase, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    return team_service.delete_team(db, body)
