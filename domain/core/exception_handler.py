from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.core.exceptions import BaseCustomException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseCustomException)
    async def custom_exception_handler(request: Request, exc: BaseCustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "code": exc.__class__.__name__}
        )

    # FastAPI 기본 HTTPException이나 다른 예외를 추가로 처리하고 싶다면 작성
