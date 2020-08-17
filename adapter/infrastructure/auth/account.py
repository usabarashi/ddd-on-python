"""アカウント
"""

from dataclasses import dataclass
from typing import Optional

import umongo
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument

from adapter.infrastructure import mongodb


@dataclass(frozen=True)
class Account:
    """DTO
    """
    username: str
    full_name: str
    email: str
    hashed_password: str


@mongodb.connector.register
class AccountDAO(MotorAsyncIODocument):
    username = umongo.fields.StringField(required=True, attribute="username")
    full_name = umongo.fields.StringField(required=True, attribute="full_name")
    email = umongo.fields.StringField(required=True, attribute="email")
    hashed_password = umongo.fields.StringField(
        required=False, attribute="hashed_password")
    disabled = umongo.fields.BooleanField(require=True, attribute="disabled")

    class Meta:
        collection_name = "account"


async def get(username: str) -> Optional[Account]:
    """アクティブアカウントを取得する
    """
    got_document = await AccountDAO.find_one(filter={"username": username})

    if got_document is None:
        return None

    got_dict = got_document.dump()
    del got_dict["id"], got_dict["disabled"]

    return Account(**got_dict)
