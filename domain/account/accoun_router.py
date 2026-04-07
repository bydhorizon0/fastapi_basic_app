from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import AsyncDbSessionDep
from domain.account import account_service
from domain.account.schemas import SignupRequest, LoginRequest, Token
from domain.core.settings import get_settings
from domain.core.utils import create_access_token, oauth2_scheme

router = APIRouter(prefix="/api/auth")


@router.post("/signup")
async def signup(db: AsyncDbSessionDep, body: SignupRequest):
    await account_service.signup(db, body)


@router.post("/token")
async def login(db: AsyncDbSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    body = LoginRequest(email=form_data.username, password=form_data.password)

    user_info = await account_service.login(db, body)

    access_token = create_access_token(
        data={"sub": user_info.email},
        expires_delta=timedelta(minutes=get_settings().access_token_expire_minute),
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
