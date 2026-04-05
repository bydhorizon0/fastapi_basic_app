from fastapi import FastAPI

from domain.account import accoun_router

# SQLAlchemy 매퍼(Mapper) 초기화 시점에 "Post" 문자열을 실제 클래스로 해석하지 못해서 발생합니다.
import domain.account.models
import domain.post.models
from domain.post import post_router

app = FastAPI()


app.include_router(router=accoun_router.router, tags=["accounts"])
app.include_router(router=post_router.router, tags=["posts"])
