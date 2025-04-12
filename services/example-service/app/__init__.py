from fastapi import FastAPI

from .dependencies import init_db, shutdown_db
from .routes.example_router import example_router


async def lifecycle_events(app: FastAPI):
    await init_db()
    yield
    await shutdown_db()


app = FastAPI(lifespan=lifecycle_events)


app.include_router(example_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
