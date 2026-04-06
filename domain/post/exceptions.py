from fastapi import status

from domain.core.exceptions import BusinessException, BaseCustomException


class PostNotFoundError(BusinessException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Post not found"


class PermissionDeniedError(BusinessException):
    status_code = 403
    detail = "수정 권한이 없습니다."
