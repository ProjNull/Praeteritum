from fastapi import Depends, Request, APIRouter
from ...database.services import vote_service
from ...database import get_session
from .services import user_service


retrospectives_router = APIRouter(prefix="/votes")


@retrospectives_router.post("/add_vote")
async def create_retro(body: vote_service.vote_schemas.AddVote, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await vote_service.add_vote(db, body, user_id)


@retrospectives_router.post("/remove_vote")
async def create_retro(body: vote_service.vote_schemas.RemoveVote, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await vote_service.remove_vote(db, body, user_id)


@retrospectives_router.post("/get_vote_count")
async def create_retro(body: vote_service.vote_schemas.GetVoteCount, db = Depends(get_session), kinde_client=Depends(user_service.get_kinde_client)):
    user_id = kinde_client.get_user_details().get("id")
    return await vote_service.get_vote_count(db, body, user_id)
