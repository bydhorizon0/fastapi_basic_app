from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from domain.account import account_repository
from domain.account.exceptions import UserNotFoundError
from domain.account.models import User
from domain.post import post_repository
from domain.post.exceptions import PostNotFoundError, PermissionDeniedError
from domain.post.models import Post
from domain.post.schemas import PostCreateRequest, PostDetailResponse, PostResponse, PostUpdateRequest


async def get_post(adb: AsyncSession, post_id: int) -> PostDetailResponse:
    post = await post_repository.get_post_by_id(adb, post_id)

    if post is None:
        raise PostNotFoundError()

    return PostDetailResponse.model_validate(post)


async def get_posts(adb: AsyncSession) -> list[PostResponse]:
    posts: list[Post] = await post_repository.get_all_posts(adb)
    return [PostResponse.model_validate(post) for post in posts]


def create_post(db: Session, request: PostCreateRequest, user_email: str) -> PostDetailResponse:
    user: User | None = account_repository.get_user_by_email(db, user_email)
    if user is None:
        raise UserNotFoundError()

    post = Post(title=request.title, content=request.content, user=user)

    # Transaction
    try:
        post_repository.insert_post(db, post)
        db.commit()
        db.refresh(post)
        return PostDetailResponse.model_validate(post)
    except Exception as e:
        db.rollback()
        raise e


async def update_post(
    adb: AsyncSession,
    request: PostUpdateRequest,
    post_id: int,
    current_user_email: str
) -> PostDetailResponse:
    post = await post_repository.get_post_by_id(adb, post_id)

    if post is None:
        raise PostNotFoundError()

    if post.user.email != current_user_email:
        raise PermissionDeniedError()

    update_data = request.model_dump(exclude_unset=True)

    # 객체 속성 업데이트
    for key, value in update_data.items():
        setattr(post, key, value)

    # dirty check 후 업데이트 쿼리가 날아감
    await adb.commit()
    # 업데이트된 최신 DB 값을 반영

    await adb.refresh(post)

    return PostDetailResponse.model_validate(post)


async def delete_post(
    adb: AsyncSession,
    post_id: int,
    current_user_email: str
):
    post = await post_repository.get_post_by_id(adb, post_id)

    if post is None:
        raise PostNotFoundError()

    if post.user.email != current_user_email:
        raise PermissionDeniedError()

    await adb.delete(post)
    await adb.commit()
