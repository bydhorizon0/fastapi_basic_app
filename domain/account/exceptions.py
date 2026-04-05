from fastapi import HTTPException, status


class UserAlreadyError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 이메일입니다."
        )


class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="유저가 존재하지 않습니다.")
