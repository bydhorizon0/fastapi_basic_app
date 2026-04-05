from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import DbSessionDep
from domain.account import account_service
from domain.account.schemas import SignupRequest, LoginRequest, Token
from domain.core.settings import get_settings
from domain.core.utils import create_access_token, oauth2_scheme

router = APIRouter(prefix="/api/auth")


@router.post("/signup")
def signup(db: DbSessionDep, body: SignupRequest):
    try:
        account_service.signup(db, body)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/token")
def login(db: DbSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        body = LoginRequest(email=form_data.username, password=form_data.password)

        user_info = account_service.login(db, body)

        access_token = create_access_token(
            data={"sub": user_info.email},
            expires_delta=timedelta(minutes=get_settings().access_token_expire_minute),
        )

        return Token(access_token=access_token, token_type="bearer")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/me")
def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
