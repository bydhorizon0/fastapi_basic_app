from abc import ABC

from fastapi import status


class BaseCustomException(ABC, Exception):
    """
    모든 도메인 예외의 기반
    추상클래스로 직접 raise BaseCustomException() 하는 것을 방지
    """

    status_code: int
    detail: str

    def __init__(self, status_code: int | None = None, detail: str | None = None):
        # 호출 시 인자가 들어오면 그걸 쓰고, 없으면 클래스 변수(기본값)를 사용한다.
        self.detail = detail or getattr(self, "detail", "Internal server error")
        self.status_code = status_code or getattr(self, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        super().__init__(self.detail)


class AuthException(BaseCustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "인증에 실패했습니다."


class BusinessException(BaseCustomException):
    status_code = 400
    detail = "Business error"
