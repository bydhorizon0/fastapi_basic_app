from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, DateTime, func, String, Text, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates, column_property

from database import Base
from domain.account.models import User


class BaseEntity(Base):
    __abstract__ = True  # __abstract__ = True 없으면 → 테이블로 인식

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Post(BaseEntity):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )  # 공백 불가능하게 하고 싶음
    content: Mapped[str] = mapped_column(Text, nullable=False)  # 공백 불가능하게 하고 싶음

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(back_populates="posts")

    comments: Mapped[list[Comment]] = relationship(
        back_populates="post", cascade="all, delete-orphan", lazy="selectin"
    )

    @validates("title", "content")
    def validate_not_blank(self, key: str, value: str) -> str:
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be blank")
        return value


class Comment(BaseEntity):
    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(Text, nullable=False)  # 공백 불가능하게 하고 싶음

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(back_populates="comments")

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    post: Mapped[Post] = relationship(back_populates="comments")

    @validates("content")
    def validate_not_blank(self, key: str, value: str) -> str:
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be blank")
        return value


Post.user_email = column_property(
    select(User.email).where(User.id == Post.user_id).correlate_except(User).scalar_subquery()
)

# Post 클래스가 정의되는 시점에 아직 Comment 클래스가 존재하지 않기 때문에 NameError 또는 Unresolved reference가 발생한다.
# 파이썬은 코드를 위에서 아래로 읽음.
Post.comment_count = column_property(
    select(func.count(Comment.id))
    .where(Comment.post_id == Post.id)
    .correlate_except(Comment)  # 성능 및 정확성을 위한 최적화
    .scalar_subquery()
)
