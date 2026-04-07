from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


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


class PostListRequest(BaseModel):
    page: int = Field(default=1, ge=1, description="페이지 번호 (1부터 시작)")
    size: int = Field(default=10, ge=1, le=100, description="한 페이지당 노출 개수 (최대 100개)")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size
