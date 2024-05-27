from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from ..config import DB_DRIVER, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

if DB_DRIVER == "postgresql":
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
elif DB_DRIVER == "sqlite":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session() -> Generator[any, any, Session]:
    """
    Returns a generator that yields a database session. The session is created using the `SessionLocal` class from the `sqlalchemy.orm` module. The session is automatically closed when the generator is exhausted.
    Usage: session = Depends(get_session)

    Returns:
        Generator[any, any, Session]: A generator that yields a database session.

    Raises:
        Exception: If an exception occurs during the execution of the generator, the session is rolled back and the exception is re-raised.
    """
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
