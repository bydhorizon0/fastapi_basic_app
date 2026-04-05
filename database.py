from typing import Annotated, Generator, AsyncGenerator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

SYNC_DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/basic?charset=utf8mb4"
ASYNC_DATABASE_URL = "mysql+aiomysql://root:root123@localhost:3306/basic?charset=utf8mb4"

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=sync_engine, autoflush=True, autocommit=False)

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None]:
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


DbSessionDep = Annotated[Session, Depends(get_db)]
AsyncDbSessionDep = Annotated[AsyncSessionLocal, Depends(get_async_db)]
