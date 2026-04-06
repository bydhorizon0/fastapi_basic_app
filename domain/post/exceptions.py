from fastapi import status

from domain.core.exceptions import BusinessException


class PostNotFoundError(BusinessException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Post not found"
