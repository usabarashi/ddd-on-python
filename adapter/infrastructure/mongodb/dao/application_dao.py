"""ApplicationDAO
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Generator, Iterable, List, Optional

import umongo
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument

from adapter.infrastructure import mongodb
from domain import application, entity


@dataclass(frozen=True)
class Progress:
    """DTO
    """
    approver_id: entity.Id
    approve: Optional[application.Judgment]
    datetime_: Optional[datetime]
    comment: Optional[str]


class ProgressDocument(umongo.Document):
    approver_id = umongo.fields.StringField()
    approve = umongo.fields.IntegerField(allow_none=True)
    datetime_ = umongo.fields.DateTimeField(allow_none=True)
    comment = umongo.fields.StrField(allow_none=True)


@dataclass(frozen=True)
class Application:
    """DTO
    """
    id_: entity.Id
    applicant_id: entity.Id
    workflow_id: entity.Id
    route: List[Progress]


@mongodb.connector.register
class ApplicationDocument(MotorAsyncIODocument):
    id_ = umongo.fields.StringField(required=True, attribute="_id")
    applicant_id = umongo.fields.StringField()
    workflow_id = umongo.fields.StringField()
    route = umongo.fields.ListField(umongo.fields.DictField(ProgressDocument))

    class Meta:
        collection_name = "application"


async def get(id_: entity.Id) -> Optional[Application]:
    got_document = await ApplicationDocument.find_one({"id_": id_})
    if got_document is None:
        return None
    return Application(**got_document.dump())


async def find() -> Generator[Application, None, None]:
    got_documents: Iterable[MotorAsyncIODocument] = await ApplicationDocument.find().to_list(
        length=10)
    return (Application(**got_document.dump()) for got_document in got_documents)
