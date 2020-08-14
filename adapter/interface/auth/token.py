# -*- coding: utf-8 -*-
"""Auth
"""

from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from adapter.auth import auth
from adapter.auth.token_dao import Token, TokenDAO
from dsl.type import Err

router = APIRouter()


class Request(BaseModel):
    username: str = ""
    password: str = ""


@router.post(
    path="/auth/token",
    tags=["auth"],
    response_model=Token,
    status_code=200,
    summary="",
    description="Sample: johndoe:password",
)
async def create_token(request: Request) -> Token:

    auth_result = await auth.authenticate(
        username=request.username, password=request.password
    )
    if isinstance(auth_result, Err):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        account = auth_result.value
        token = await auth.create_token(key=account.username, expires_delta=None)
        return token


@router.get(
    path="/auth/token",
    tags=["auth"],
    response_model=List[Token],
    status_code=200,
    summary="",
    description="Management.",
)
async def find_token() -> List[Token]:
    return await TokenDAO.find()
