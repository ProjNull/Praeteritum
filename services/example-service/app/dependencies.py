from typing import Annotated, AsyncGenerator

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from redis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from .config import settings

engine = create_async_engine(settings.postgres_url)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get a database session.

    This is a context manager that can be used in a FastAPI dependency. It
    will create a new session and yield it to the dependency. When the
    dependency is exited, it will roll back the session.

    Yields:
        AsyncSession: A database session.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def shutdown_db() -> None:
    await engine.dispose()


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_redis() -> AsyncGenerator[Redis, None]:
    """
    Dependency to get a Redis connection.

    This is a context manager that can be used in a FastAPI dependency. It
    will create a new Redis connection the first time it's called and yield it to
    the dependency. When the dependency is exited, it will close the Redis connection.

    Yields:
        Redis: A Redis connection.
    """
    try:
        redis = Redis.from_url(settings.redis_url)
        yield redis
    finally:
        redis.close()


RedisDep = Annotated[Redis, Depends(get_redis)]


async def get_kafka_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    try:
        producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers, request_timeout_ms=5000)
        yield producer
    finally:
        await producer.stop()


async def get_kafka_consumer() -> AsyncGenerator[AIOKafkaConsumer, None]:
    try:
        consumer = AIOKafkaConsumer(
            "example_topic", bootstrap_servers=settings.kafka_bootstrap_servers, request_timeout_ms=5000
        )
        yield consumer
    finally:
        await consumer.stop()


KafkaProducerDep = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
KafkaConsumerDep = Annotated[AIOKafkaConsumer, Depends(get_kafka_consumer)]
