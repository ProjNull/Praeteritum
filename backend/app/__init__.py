from fastapi import FastAPI
from .database import get_session

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# You can import and include your routes here if you have any
from .routes import router as routes_router
app.include_router(routes_router)

