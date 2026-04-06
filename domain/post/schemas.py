from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostCreateRequest(BaseModel):
    title: str
    content: str


class PostUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None


class PostResponse(BaseModel):
    title: str
    content: str
    user_email: str
    comment_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostDetailResponse(BaseModel):
    title: str
    content: str
    user_email: str
    # comment 추후 추가
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
