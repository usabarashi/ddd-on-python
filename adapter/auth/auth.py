# -*- coding: utf-8 -*-
"""Auth

see: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""

from typing import Literal, Optional
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from adapter.auth.account_dao import Account, AccountDAO
from dsl.type import Err, Ok, Result

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate(username: str, password: str) -> Result[Literal[False], Account]:
    """認証
    """
    account = await AccountDAO.get(username=username)
    if not account or not verify_password(
        plain_password=password, hashed_password=account.hashed_password
    ):
        return Err(value=False)
    else:
        return Ok(value=account)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワード照合
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_token(
    data: dict,
    expires_delta: Optional[timedelta] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    """トークン生成
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def to_hash(string: str) -> str:
    """ハッシュ化
    """
    return pwd_context.hash(string)
