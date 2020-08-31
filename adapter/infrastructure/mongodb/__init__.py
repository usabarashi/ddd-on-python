"""MongoDB

ODM:
    uMongo: https://umongo.readthedocs.io/en/latest/index.html
Driver:
    motor: https://docs.mongodb.com/drivers/motor
"""
from typing import TypeVar

import ulid
from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance

from adapter import config
from domain import entity

_S = TypeVar("_S")  # Self


class ULID(entity.Id, str):
    """ULID

    ObjectId:
        https://docs.mongodb.com/manual/reference/method/ObjectId/

    ULID:
        https://ja.wikipedia.org/wiki/UUID
    """

    def __init__(self: _S,  value: str) -> _S:
        # Validation
        ulid.from_str(value)

        str.__init__(value)

    def __eq__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) == ulid.from_str(other)

    def __ne__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) != ulid.from_str(other)

    def __hash__(self: _S) -> int:
        return hash(ulid.from_str(self))

    def __lt__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) < ulid.from_str(other)

    def __le__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) <= ulid.from_str(other)

    def __gt__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) > ulid.from_str(other)

    def __ge__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) >= ulid.from_str(other)

    @classmethod
    def generate(cls: _S) -> _S:
        return __class__(ulid.new().str)


def _create_connector() -> Instance:
    uri: str = config["adapter"]["infrastructure"]["mongodb"]["URI"]
    database: str = "enterprise"
    client: AsyncIOMotorClient = AsyncIOMotorClient(uri)
    return Instance(client[database])


connector = _create_connector()
