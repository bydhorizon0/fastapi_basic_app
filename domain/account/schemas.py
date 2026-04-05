from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, model_validator, EmailStr, ConfigDict


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def check_password(self) -> SignupRequest:
        if self.password != self.password_repeat:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return self

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
