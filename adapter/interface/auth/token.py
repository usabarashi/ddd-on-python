"""Auth
"""

from dataclasses import asdict, dataclass
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import BaseModel

from adapter.infrastructure.auth import auth, token_dao
from dsl.type import Err

router = APIRouter()


@dataclass(frozen=True)
class ResponseToken(BaseModel, token_dao.Token):
    access_token: str
    token_type: str


@router.get(
    path="/auth/token",
    tags=["auth"],
    response_model=List[ResponseToken],
    status_code=200,
    summary="",
    description="Management.",
)
async def find_token():
    return [ResponseToken(**asdict(got_token)) async for got_token in token_dao.find()]


@router.post(
    path="/auth/token",
    tags=["auth"],
    response_model=ResponseToken,
    status_code=200,
    summary="",
    description="Sample: johndoe/password",
)
async def create_token(request: OAuth2PasswordRequestForm = Depends()):

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
        authed_account = auth_result.value
        created_token = await auth.create_token(key=authed_account.id_, expires_delta=None)
        return ResponseToken(**asdict(created_token))
