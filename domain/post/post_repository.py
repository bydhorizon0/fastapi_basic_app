from typing import cast, Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.account.models import User
from domain.post.models import Post, Comment


async def get_post_by_id(db: AsyncSession, post_id: int) -> Post | None:
    result = await db.execute(
        select(Post).where(Post.id == post_id).options(selectinload(Post.user))
    )

    return result.scalar_one_or_none()


async def get_all_posts(db: AsyncSession, limit: int = 10, offset: int = 0) -> list[dict]:
    # user 정보를 미리 로드 (Eager Loading), N+1 방지
    result = await db.execute(
        select(
            Post.title,
            Post.content,
            User.email.label("user_email"),
            func.count(Comment.id).label("comment_count"),
            Post.created_at,
            Post.updated_at,
        )
        .join(Post.user)
        .outerjoin(Post.comments)
        .group_by(Post.id, User.email)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return [dict(row) for row in result.mappings().all()]


async def insert_post(db: AsyncSession, post: Post):
    db.add(post)
    await db.flush()  # ID 등 임시 반영, 커밋은 서비스에서 결정
    return post
