from typing import Annotated

from fastapi import APIRouter, Depends, status

from database import AsyncDbSessionDep, DbSessionDep
from domain.core.utils import get_current_user
from domain.post import post_service
from domain.post.schemas import PostCreateRequest, PostDetailResponse, PostResponse, PostUpdateRequest

router = APIRouter(prefix="/api/posts")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PostResponse])
async def posts(adb: AsyncDbSessionDep):
    return await post_service.get_posts(adb)


@router.get("/{post_id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostDetailResponse)
async def post(adb: AsyncDbSessionDep, post_id: int):
    return await post_service.get_post(adb, post_id)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=PostDetailResponse)
def create(
    db: DbSessionDep,
    request: PostCreateRequest,
    current_user_email: Annotated[str, Depends(get_current_user)],
):
    return post_service.create_post(db, request, current_user_email)


@router.patch("/{post_id}", status_code=status.HTTP_200_OK)
async def update(
    adb: AsyncDbSessionDep,
    request: PostUpdateRequest,
    post_id: int,
    current_user_email: Annotated[str, Depends(get_current_user)]
):
    await post_service.update_post(adb, request, post_id, current_user_email)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    adb: AsyncDbSessionDep,
    post_id: int,
    current_user_email: Annotated[str, Depends(get_current_user)]
):
    await post_service.delete_post(adb, post_id, current_user_email)
