from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.account.models import User


async def exists_email(db: AsyncSession, email: str) -> bool:
    result: bool | None = await db.scalar(select(exists().where(User.email == email)))
    return result if result is not None else False


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email))
