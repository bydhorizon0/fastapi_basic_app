from fastapi import status

from domain.core.exceptions import AuthException, BusinessException


class UserAlreadyError(BusinessException):
    status_code = status.HTTP_409_CONFLICT
    detail = "이미 존재하는 이메일입니다."


class UserNotFoundError(AuthException):
    detail = "계정을 찾을 수 없습니다."


class LoginFailedError(AuthException):
    detail = "아이디 또는 비밀번호가 일칯하지 않습니다."
