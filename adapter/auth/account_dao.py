# -*- coding: utf-8 -*-
"""アカウントDAO
"""

from dataclasses import dataclass
from typing import Optional

_fake_account_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        # "plain_password": "password",
        "hashed_password": "$2b$12$zfo4.zaRPiE4ArMukvG/.u4hHX1J0R3WKbIQLFliGqUURxthctyZ2",
        "disabled": False,
    }
}


@dataclass(frozen=True)
class Account:
    username: str
    full_name: str
    hashed_password: str
    email: Optional[str] = None
    disabled: Optional[bool] = None


class AccountDAO:
    @staticmethod
    async def get(username: str) -> Optional[Account]:
        global _fake_account_db
        if username not in _fake_account_db:
            return None
        else:
            return Account(**_fake_account_db[username])

