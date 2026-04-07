import asyncio

from faker.proxy import Faker
from sqlalchemy import select

from database import AsyncSessionLocal
from domain.account.models import User
from domain.post.models import Post


async def seed_db(count=300) -> None:
    fake = Faker()

    async with AsyncSessionLocal() as session:
        async with session.begin():
            posts: list[Post] = []

            result = await session.execute(select(User).where(User.email == "jack95@example.com"))
            user: User | None = result.scalar_one_or_none()

            if user is None:
                raise Exception("해당하는 유저가 없습니다.")

            for _ in range(count):
                post = Post(title=fake.paragraph(), content=fake.text(), user=user)

                posts.append(post)

            session.add_all(posts)
        await session.commit()
        print(f"{count}개의 더미 데이터 삽입 완료!")


if __name__ == "__main__":
    asyncio.run(seed_db())
