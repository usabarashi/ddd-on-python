"""トークンDAO
"""
from dataclasses import asdict, dataclass
from typing import Generator, Iterable, Optional

import umongo
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument

from adapter.infrastructure import mongodb


@dataclass(frozen=True)
class Token:
    """DTO
    """
    access_token: str
    token_type: str


@mongodb.connector.register
class TokenDAO(MotorAsyncIODocument):
    access_token = umongo.fields.StringField(required=True)
    token_type = umongo.fields.StringField(required=True)

    class Meta:
        collection_name = "token"


async def get(access_token: str) -> Optional[Token]:
    got_document = await TokenDAO.find_one(kwargs={"access_token": access_token})

    if got_document is None:
        return None

    got_dict = got_document.dump()
    del got_dict["id"]
    return Token(**got_document.dump())


async def find() -> Generator[Token, None, None]:
    got_documents: Iterable[MotorAsyncIODocument] = await TokenDAO.find().to_list(length=10)
    for got_document in got_documents:
        got_dict = got_document.dump()
        del got_dict["id"]
        yield Token(**got_dict)


async def save(entity: Token) -> Token:
    document_entity = TokenDAO(**asdict(entity))
    await document_entity.commit()
    return entity
