"""AcountDAO
"""

from dataclasses import dataclass
from typing import Iterable, Generator, Optional

import umongo
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument

from adapter.infrastructure import mongodb


@dataclass(frozen=True)
class Account:
    """DTO
    """
    username: str
    full_name: str
    hashed_password: str
    email: Optional[str] = None
    disabled: Optional[bool] = None


@mongodb.connector.register
class AccountDAO(MotorAsyncIODocument):
    username = umongo.fields.StringField(required=True, attribute="username")
    full_name = umongo.fields.StringField(required=True, attribute="full_name")
    email = umongo.fields.StringField(required=True, attribute="email")
    hashed_password = umongo.fields.StringField(
        required=False, attribute="hashed_password")
    disabled = umongo.fields.BooleanField(required=False, attribute="disabled")

    class Meta:
        collection_name = "account"


async def find() -> Generator[Account, None, None]:
    documents: Iterable[MotorAsyncIODocument] = await AccountDAO.find().to_list(length=10)
    for document in documents:
        got_dict = document.dump()
        del got_dict["id"]
        yield Account(**got_dict)
