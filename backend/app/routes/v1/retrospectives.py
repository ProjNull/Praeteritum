from fastapi import Depends, Request, APIRouter
from ...database.services import retro_service
from ...database import get_session

retrospectives_router = APIRouter(prefix="/retrospectives")

@retrospectives_router.post("/create_retro")
def create_retro(body: retro_service.retro_schemas.RetroCreate, db = Depends(get_session)):
    return retro_service.create_retro(db, body)

@retrospectives_router.get("/get_retro_by_id")
def get_retro_by_id(body: retro_service.retro_schemas.QueryRetro, db = Depends(get_session)):
    return retro_service.get_retro_by_id(db, body)

@retrospectives_router.get("/get_all_retros_in_org")
def get_all_retros_in_org(body: retro_service.retro_schemas.QueryAllRetrosInOrganization, db = Depends(get_session)):
    return retro_service.get_all_retros_in_org(db, body)

@retrospectives_router.get("/get_all_retros_by_user")
def get_all_retros_by_user(body: retro_service.retro_schemas.QueryAllRetrosForUser, db = Depends(get_session)):
    return retro_service.get_all_retros_by_user(db, body)

@retrospectives_router.get("/fetch_retros")
def fetch_retros(body: retro_service.retro_schemas.QueryRetroList, db = Depends(get_session)):
    return retro_service.fetch_retros(db, body)

@retrospectives_router.delete("/delete_retro")
def delete_retro(body: retro_service.retro_schemas.QueryRetro, db = Depends(get_session)):
    return retro_service.delete_retro(db, body)

@retrospectives_router.patch("/update_retro")
def update_retro(body: retro_service.retro_schemas.RetroUpdate, db = Depends(get_session)):
    return retro_service.update_retro(db, body)

@retrospectives_router.get("/get_retro_members")
def get_retro_members(body: retro_service.retro_schemas.QueryRetro, db = Depends(get_session)):
    return retro_service.get_retro_members(db, body)

@retrospectives_router.post("/add_user_to_retro")
def add_user_to_retro(body: retro_service.retro_schemas.UserToRetro, db = Depends(get_session)):
    return retro_service.add_user_to_retro(db, body)

@retrospectives_router.delete("/remove_user_from_retro")
def remove_user_from_retro(body: retro_service.retro_schemas.UserToRetro, db = Depends(get_session)):
    return retro_service.remove_user_from_retro(db, body)
