# -*- coding: utf-8 -*-
"""トークンDAO
"""

from dataclasses import asdict
from typing import List, Optional


from pydantic import BaseModel


class Token(BaseModel):
    access_token: str = ""
    token_type: str = ""


_fake_token_db: List[Token] = []


class TokenRepository:
    @staticmethod
    async def get(access_token: str) -> Optional[Token]:
        global _fake_token_db
        find_result = [
            token for token in _fake_token_db if access_token == token.access_token
        ]
        if len(find_result):
            return None
        else:
            return find_result[0]

    @staticmethod
    async def find() -> List[Token]:
        global _fake_token_db
        return _fake_token_db

    @staticmethod
    async def save(entity: Token) -> Token:
        global _fake_token_db
        _fake_token_db.append(entity)
        return entity
