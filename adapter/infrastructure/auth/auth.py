# -*- coding: utf-8 -*-
"""Auth

see: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Literal, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from adapter.infrastructure.auth.account_dao import Account, AccountDAO
from adapter.infrastructure.auth.token_dao import Token, TokenDAO
from dsl.type import Err, Ok, Result

# to get a string like this run:
# openssl rand -hex 32
TOKEN_URL = "/auth/token"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


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


async def create_token(
    key: str,
    expires_delta: Optional[timedelta] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> Token:
    """トークン生成
    """
    to_encode: Dict[str, Any] = {"sub": key}.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    created_token = Token(
        access_token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM),
        token_type="bearer",
    )
    saved_token = await TokenDAO.save(entity=created_token)
    return saved_token


def to_hash(string: str) -> str:
    """ハッシュ化
    """
    return pwd_context.hash(string)


async def get_account(token: str = Depends(oauth2_scheme)) -> Account:
    """アカウント取得
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode jwt
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Get account
    account = await AccountDAO.get(username=username)
    if account is None:
        raise credentials_exception
    if account.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return account
