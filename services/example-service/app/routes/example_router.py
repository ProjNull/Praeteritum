from fastapi import APIRouter

example_router = APIRouter(
    prefix="/example",
    tags=["example"],
    responses={404: {"description": "Not found"}},
)


@example_router.get("/")
async def root():
    return {"message": "Hello World"}


from app.models.example_model import Example, ExampleUpdate, ExampleCreate
from app.services.example_service import ExampleServiceDep


@example_router.get("/all", response_model=list[Example])
async def get_all(examples: ExampleServiceDep):
    return await examples.get_all()


@example_router.get("/{id}", response_model=Example)
async def get_one(id: int, examples: ExampleServiceDep):
    return await examples.get(id)


@example_router.post("/", response_model=Example)
async def create_one(example: ExampleCreate, examples: ExampleServiceDep):
    return await examples.create(example)


@example_router.put("/{id}", response_model=Example)
async def update_one(id: int, example: ExampleUpdate, examples: ExampleServiceDep):
    return await examples.update(example, id)


@example_router.delete("/{id}", status_code=204)
async def delete_one(id: int, examples: ExampleServiceDep):
    return await examples.delete(id)
