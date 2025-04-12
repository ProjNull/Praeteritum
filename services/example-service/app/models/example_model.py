from sqlmodel import SQLModel, Field


class ExampleBase(SQLModel):
    name: str


class ExampleUpdate(ExampleBase):
    pass


class ExampleCreate(ExampleUpdate):
    pass


class Example(ExampleCreate, table=True):
    id: int = Field(default=None, primary_key=True)
