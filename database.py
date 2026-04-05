from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/basic?charset=utf8mb4"

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None]:
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()


DbSessionDep = Annotated[Session, Depends(get_db)]
