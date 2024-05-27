from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# You can import and include your routes here if you have any
from .routes import router as routes_router
app.include_router(routes_router)

