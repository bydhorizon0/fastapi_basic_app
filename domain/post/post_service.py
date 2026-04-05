from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from domain.account import account_repository
from domain.account.exceptions import UserNotFoundError
from domain.account.models import User
from domain.post import post_repository
from domain.post.models import Post
from domain.post.schemas import PostCreateRequest, PostDetailResponse, PostResponse


async def get_posts(adb: AsyncSession) -> list[PostResponse]:
    posts: list[Post] = await post_repository.get_all_posts(adb)
    return [PostResponse.model_validate(post) for post in posts]


def create_post(db: Session, body: PostCreateRequest, user_email: str) -> PostDetailResponse:
    user: User | None = account_repository.get_user_by_email(db, user_email)
    if user is None:
        raise UserNotFoundError()

    post = Post(title=body.title, content=body.content, user=user)

    # Transaction
    try:
        post_repository.insert_post(db, post)
        db.commit()
        db.refresh(post)
        return PostDetailResponse.model_validate(post)
    except Exception as e:
        db.rollback()
        raise e
