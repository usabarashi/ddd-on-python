"""AcountDAO
"""

from dataclasses import dataclass
from typing import Generator, Optional

from umongo import Document, fields

from adapter.infrastructure.datastore.mongo import connector


@dataclass(frozen=True)
class Account:
    username: str
    full_name: str
    hashed_password: str
    email: Optional[str] = None
    disabled: Optional[bool] = None


@connector.register
class AccountDAO(Document):
    class Meta:
        collection_name = "account"

    username = fields.StringField(required=True, attribute="username")
    full_name = fields.StringField(required=True, attribute="full_name")
    email = fields.StringField(required=True, attribute="email")
    hashed_password = fields.StringField(required=False, attribute="hashed_password")
    disabled = fields.BooleanField(required=False, attribute="disabled")

    @classmethod
    async def find(cls) -> Generator[Account, None, None]:
        return (
            Account(**account_doc)
            for account_doc in await super(AccountDAO, cls)
            .find({}, limit=10, skip=0)
            .to_list(length=1)
        )
