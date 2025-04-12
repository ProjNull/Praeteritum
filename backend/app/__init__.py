from fastapi import FastAPI

from .database import get_session

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


from .routes import api_router

app.include_router(api_router)
