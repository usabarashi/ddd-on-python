"""Account
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
    full_name: str
    email: str
    hashed_password: str


@mongodb.connector.register
class AccountDocument(MotorAsyncIODocument):
    """
    e.g.:
        {
            _id: ULID,
            username: 'johndoe',
            full_name: 'John Doe',
            email: 'johndoe@example.com',
            // plain_password: password
            hashed_password: '$2b$12$zfo4.zaRPiE4ArMukvG/.u4hHX1J0R3WKbIQLFliGqUURxthctyZ2',
            disabled: false
        }
    """
    id_ = umongo.fields.StringField(required=True, attribute="_id")
    username = umongo.fields.StringField(required=True)
    full_name = umongo.fields.StringField(required=True)
    email = umongo.fields.StringField(required=True)
    hashed_password = umongo.fields.StringField(required=False)
    disabled = umongo.fields.BooleanField(require=True)

    class Meta:
        collection_name = "account"


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
