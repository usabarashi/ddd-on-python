# -*- coding: utf-8 -*-
"""MongoDB

see:
    uMongo: https://umongo.readthedocs.io/en/latest/apireference.html# 
"""
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance

USERNAME: str = "root"
PASSWORD: str = "password"
HOST: str = "datastore"
PORT: int = 27017
DATABASE: str = "enterprise"
URI: str = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"


def create_connector() -> Instance:
    loop = asyncio.get_event_loop()
    database_connector = loop.run_until_complete(
        future=_connect_database(database=DATABASE)
    )
    return Instance(database_connector)


async def _connect_database(database: str):
    client = AsyncIOMotorClient(URI)
    return client[database]


connector = create_connector()
