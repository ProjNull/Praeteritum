from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.dependencies import RedisDep, SessionDep
from app.exceptions.example_exceptions import ExampleNotFoundException
from app.models.example_model import Example, ExampleBase


class ExampleService:
    def __init__(self, session: SessionDep, redis: RedisDep):
        self.session: AsyncSession = session
        self.redis: Redis = redis
        self.redis_expire_seconds = 300  # 5 minutes

    def _example_cache_key(self, id: int) -> str:
        return f"example:{id}"

    def _examples_list_key(self) -> str:
        return "examples"

    async def get(self, id: int) -> Example:
        cache_key = self._example_cache_key(id)
        cached = self.redis.get(cache_key)
        if cached:
            try:
                return Example.model_validate_json(cached)
            except Exception:
                self.redis.delete(cache_key)  # corrupted cache? purge it

        example = await self.session.get(Example, id)
        if not example:
            raise ExampleNotFoundException(id)

        self.redis.set(
            cache_key, example.model_dump_json(), ex=self.redis_expire_seconds
        )
        return example

    async def get_all(self) -> list[Example]:
        list_key = self._examples_list_key()
        cached = self.redis.lrange(list_key, 0, -1)
        if cached:
            try:
                return [Example.model_validate_json(item) for item in cached]
            except Exception:
                self.redis.delete(list_key)

        statement = select(Example)
        result = await self.session.execute(statement)
        examples = result.scalars().all()

        if examples:
            self.redis.lpush(list_key, *[ex.model_dump_json() for ex in examples])
            self.redis.expire(list_key, self.redis_expire_seconds)

        return examples

    async def create(self, example: ExampleBase) -> Example:
        obj = Example.model_validate(example)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

        self.redis.delete(self._examples_list_key())
        self.redis.set(
            self._example_cache_key(obj.id),
            obj.model_dump_json(),
            ex=self.redis_expire_seconds,
        )

        return obj

    async def update(self, example: ExampleBase, id: int) -> Example:
        db_obj = await self.session.get(Example, id)
        if not db_obj:
            raise ExampleNotFoundException(id)

        for key, value in example.model_dump(exclude_unset=True).items():
            setattr(db_obj, key, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        self.redis.delete(self._examples_list_key())
        self.redis.set(
            self._example_cache_key(id),
            db_obj.model_dump_json(),
            ex=self.redis_expire_seconds,
        )

        return db_obj

    async def delete(self, id: int) -> None:
        db_obj = await self.session.get(Example, id)
        if not db_obj:
            raise ExampleNotFoundException(id)

        await self.session.delete(db_obj)
        await self.session.commit()

        self.redis.delete(self._example_cache_key(id))
        self.redis.delete(self._examples_list_key())


ExampleServiceDep = Annotated[ExampleService, Depends(ExampleService)]
