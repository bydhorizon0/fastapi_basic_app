from datetime import datetime
from typing import Literal, Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


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


class PostListResponse(BaseModel):
    items: list[PostResponse]  # 게시글 목록
    total_count: int  # 전체 게시글 수
    page: int  # 현재 페이지
    size: int  # 페이지당 개수


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
    search_keyword: str = Field(default="", description="검색 키워드 (양 끝 공백 자동 제거)")
    search_type: Literal["t", "c", "w", "tc"] = "t"

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    # 이 모델의 모든 str 필드는 자동으로 strip 처리됨
    model_config = ConfigDict(
        str_strip_whitespace=True
    )
