from typing import cast, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, Session

from domain.post.models import Post


async def get_post_by_id(adb: AsyncSession, post_id: int) -> Post | None:
    result = await adb.execute(
        select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(Post.user)
        )
    )

    return result.scalar_one_or_none()


async def get_all_posts(adb: AsyncSession) -> list[Post]:
    # user 정보를 미리 로드 (Eager Loading), N+1 방지
    result = await adb.execute(
        select(Post)
        .options(
            selectinload(Post.user)
        )
        .order_by(Post.created_at.desc())
    )

    # selectinload나 joinedload 같은 Eager Loading을 사용할 때, 간혹 결과 집합에 중복된 객체가 포함될 수 있다 (1:N 관계 등).
    # 비동기 환경에서는 .unique()를 호출해 주는 것이 안전하다.

    # all(): 이 메서드는 실제 데이터를 메모리로 모두 가져와 list 형태로 반환하지만,
    # 타입 정의상으로는 여전히 상위 개념인 Sequence로 잡히는 경우가 많다.

    # scalars()는 여러 종류의 객체가 섞여 있을 가능성을 열어두기 때문에 제네릭하게 Any를 포함한 Sequence를 반환한다.
    return list(cast(Sequence[Post], result.unique().scalars().all()))


def insert_post(db: Session, post: Post):
    db.add(post)
    db.flush()  # ID 등 임시 반영, 커밋은 서비스에서 결정
    return post
