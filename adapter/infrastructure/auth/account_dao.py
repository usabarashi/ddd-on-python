"""Account

EmployeeCollectionを参照して認証に必要なAccount情報だけ取得する.
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
    id_: str
    username: str
    hashed_password: str


@mongodb.connector.register
class AccountDocument(MotorAsyncIODocument):
    id_ = umongo.fields.StringField(required=True, attribute="_id")
    username = umongo.fields.StringField(required=True)
    hashed_password = umongo.fields.StringField(required=False)
    disabled = umongo.fields.BooleanField(require=True)

    class Meta:
        collection_name = "employee"


async def get(id_: str) -> Optional[Account]:
    """アクティブアカウントを取得する
    """
    got_document = await AccountDocument.find_one(filter={
        "_id": id_,
        "disabled": False,
    })

    if got_document is None:
        return None

    got_dict = got_document.dump()
    del got_dict['disabled']
    return Account(**got_dict)


async def find(username: str) -> Optional[Account]:
    """アクティブアカウントを取得する
    """
    got_document = await AccountDocument.find_one(filter={
        "username": username,
        "disabled": False,
    })

    if got_document is None:
        return None

    got_dict = got_document.dump()
    del got_dict['disabled']
    return Account(**got_dict)
