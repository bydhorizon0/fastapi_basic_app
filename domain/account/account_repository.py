from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from domain.account.models import User


def exists_email(db: Session, email: str) -> bool:
    result: bool | None = db.scalar(select(exists().where(User.email == email)))
    return result if result is not None else False


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))
