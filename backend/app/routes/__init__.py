from fastapi import APIRouter

router = APIRouter()

@router.get("/sussy/{sussy_id}")
async def sus(sussy: int):
    ...