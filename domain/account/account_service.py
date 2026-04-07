from sqlalchemy.ext.asyncio import AsyncSession

from domain.account import account_repository
from domain.account.exceptions import UserAlreadyError, UserNotFoundError
from domain.account.models import User
from domain.account.schemas import SignupRequest, LoginRequest, UserResponse
from domain.core.utils import hash_password, verify_password


async def signup(db: AsyncSession, body: SignupRequest):
    if await account_repository.exists_email(db, body.email):
        raise UserAlreadyError()

    user = User(
        **body.model_dump(exclude={"password", "password_repeat"}),
        hashed_password=hash_password(body.password),
    )

    db.add(user)
    await db.commit()


async def login(db: AsyncSession, body: LoginRequest):
    user = await account_repository.get_user_by_email(db, body.email)

    if user is None:
        raise UserNotFoundError()

    if not verify_password(body.password, user.hashed_password):
        raise UserNotFoundError()

    return UserResponse.model_validate(user)
