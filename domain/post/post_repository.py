from typing import Sequence

from sqlalchemy import select, func, or_, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.account.models import User
from domain.post.models import Post, Comment


async def get_post_by_id(db: AsyncSession, post_id: int) -> Post | None:
    result = await db.execute(
        select(Post).where(Post.id == post_id).options(selectinload(Post.user))
    )

    return result.scalar_one_or_none()


async def get_all_posts(
    db: AsyncSession,
    search_keyword: str,
    search_type: str,
    limit: int = 10,
    offset: int = 0,
) -> tuple[Sequence[RowMapping], int]:
    filters = []
    needs_user_join = False

    if search_keyword:
        match search_type:
            case "t":
                filters.append(Post.title.contains(search_keyword))
            case "c":
                filters.append(Post.content.contains(search_keyword))
            case "w":
                filters.append(User.email.contains(search_keyword))
                needs_user_join = True
            case "tc":
                filters.append(
                    or_(
                        Post.title.contains(search_keyword),
                        Post.content.contains(search_keyword),
                    )
                )

    # 전체 개수 구하기
    count_stmt = select(func.count(Post.id))
    # 이메일 검색일 때만 Join 추가
    if needs_user_join:
        count_stmt = count_stmt.join(Post.user)

    count_stmt = count_stmt.where(*filters)
    total_count = (await db.execute(count_stmt)).scalar_one()

    data_stmt = (
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
        .where(*filters)
        .group_by(Post.id, User.email)
        .order_by(Post.created_at.desc(), Post.id.desc())
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(data_stmt)
    # result.mapping() 를 호출하면 각 행(Row)은 Row 객체가 아닌 RowMapping 객체로 반환된다.
    # 이 객체는 파이썬의 Mapping 추상 베이스 클래스를 상속받아 구현됐다.
    # Mapping 타입: dict 처럼 키-값 쌍으로 데이터에 접근할 수 있는 객체를 의미한다.
    return list(result.mappings().all()), total_count


async def insert_post(db: AsyncSession, post: Post):
    db.add(post)
    await db.flush()  # ID 등 임시 반영, 커밋은 서비스에서 결정
    return post
