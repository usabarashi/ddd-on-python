"""Auth

see: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Literal, Optional

from adapter import config
from adapter.infrastructure.auth import account_dao, token_dao
from dsl.type import Err, Ok, Result
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# to get a string like this run:
# openssl rand -hex 32
CREATE_TOKEN_ENDPOINT: str = config["adapter"]["infrastructure"]["auth"][
    "CREATE_TOKEN_ENDPOINT"
]
SECRET_KEY: str = config["adapter"]["infrastructure"]["auth"]["SECRET_KEY"]
ALGORITHM: str = config["adapter"]["infrastructure"]["auth"]["ALGORITHM"]
EXPIRE_MINUTES: int = config["adapter"]["infrastructure"]["auth"]["EXPIRE_MINUTES"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=CREATE_TOKEN_ENDPOINT)


async def authenticate(
    username: str, password: str
) -> Result[Literal[False], account_dao.Account]:
    """認証
    """
    got_account = await account_dao.find(username=username)
    if got_account is None or not verify_password(
        plain_password=password, hashed_password=got_account.hashed_password
    ):
        return Err(value=False)
    else:
        return Ok(value=got_account)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワード照合
    """
    return pwd_context.verify(plain_password, hashed_password)


async def create_token(
    key: str, expires_delta: Optional[timedelta] = timedelta(minutes=EXPIRE_MINUTES)
) -> token_dao.Token:
    """トークン生成
    """
    to_encode: Dict[str, Any] = {"sub": key}.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    created_token = token_dao.Token(
        access_token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM),
        token_type="bearer",
    )
    saved_token = await token_dao.save(entity=created_token)
    return saved_token


def to_hash(string: str) -> str:
    """ハッシュ化
    """
    return pwd_context.hash(string)


async def get_id(token: str = Depends(oauth2_scheme)) -> str:
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
        id_ = payload.get("sub")
        if id_ is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Get active account
    got_active_account = await account_dao.get(id_=id_)
    if got_active_account is None:
        raise credentials_exception

    return got_active_account.id_
