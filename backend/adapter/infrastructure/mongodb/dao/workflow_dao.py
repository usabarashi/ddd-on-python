"""WorkflowDAO
"""

from dataclasses import dataclass
from typing import Generator, Iterable, Optional

import umongo
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument

from adapter.infrastructure import mongodb
from domain import entity


@dataclass(frozen=True)
class Workflow:
    """DTO
    """

    id_: str
    name: str
    description: str
    duties: int


@mongodb.connector.register
class WorkflowDocument(MotorAsyncIODocument):
    id_ = umongo.fields.StringField(attribute="_id")
    name = umongo.fields.StringField()
    description = umongo.fields.StringField()
    duties = umongo.fields.IntField()

    class Meta:
        collection_name = "workflow"


async def get(id_: entity.Id) -> Optional[Workflow]:
    got_document = await WorkflowDocument.find_one({"id_": id_})
    if got_document is None:
        return None
    return Workflow(**got_document.dump())


async def find() -> Generator[Workflow, None, None]:
    got_documents: Iterable[
        MotorAsyncIODocument
    ] = await WorkflowDocument.find().to_list(length=10)
    return (Workflow(**got_document.dump()) for got_document in got_documents)
