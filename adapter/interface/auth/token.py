# -*- coding: utf-8 -*-
"""Auth
"""

from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from adapter.auth import auth
from adapter.auth.token_repository import Token, TokenRepository
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
    description="Sample<br/>  username: johndoe<br/>  password: password",
)
async def create_token(request: Request) -> Token:

    result = await auth.authenticate(
        username=request.username, password=request.password
    )
    if isinstance(result, Err):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        created_token = Token(
            access_token=auth.create_token(
                data={"sub": result.value.username}, expires_delta=None
            ),
            token_type="bearer",
        )
        saved_token = await TokenRepository.save(entity=created_token)
        return saved_token


@router.get(
    path="/auth/token",
    tags=["auth"],
    response_model=List[Token],
    status_code=200,
    summary="",
    description="",
)
async def find_token() -> List[Token]:
    return await TokenRepository.find()
