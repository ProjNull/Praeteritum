from fastapi import Depends, Request, APIRouter
from ...database.services import board_service
from ...database import get_session

boards_router = APIRouter(prefix="/boards") # TODO: Register in init file

# Example endpoint - needs implementation
@boards_router.post("/endpoint")
def invite_user(body: board_service.board_schemas.sus, db = Depends(get_session)):
    return board_service.invite_user(db, body)
