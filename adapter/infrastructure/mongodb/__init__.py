"""MongoDB

ODM:
    uMongo: https://umongo.readthedocs.io/en/latest/index.html
Driver:
    motor: https://docs.mongodb.com/drivers/motor
"""

from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance

from adapter import config


_DATABASE: str = "enterprise"
_URI: str = config["adapter"]["infrastructure"]["mongo"]["URI"]


def _create_connector() -> Instance:
    client: AsyncIOMotorClient = AsyncIOMotorClient(_URI)
    return Instance(client[_DATABASE])


connector = _create_connector()
