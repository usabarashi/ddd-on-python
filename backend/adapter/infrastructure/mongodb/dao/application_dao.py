"""ApplicationDAO
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Generator, Iterable, List, Optional

import umongo
from adapter.infrastructure import mongodb
from domain import application, entity
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument


@dataclass(frozen=True)
class Progress:
    """DTO
    """

    approver_id: str
    approve: Optional[application.Judgment]
    process_datetime: Optional[datetime]
    comment: Optional[str]


@dataclass(frozen=True)
class Application:
    """DTO
    """

    id_: str
    applicant_id: str
    workflow_id: str
    route: List[Progress]


@mongodb.connector.register
class ProgressDocument(umongo.EmbeddedDocument):
    approver_id = umongo.fields.StrField()
    approve = umongo.fields.IntegerField(allow_none=True)
    process_datetime = umongo.fields.DateTimeField(allow_none=True)
    comment = umongo.fields.StrField(allow_none=True)


@mongodb.connector.register
class ApplicationDocument(MotorAsyncIODocument):
    id_ = umongo.fields.StringField(required=True, attribute="_id")
    applicant_id = umongo.fields.StringField()
    workflow_id = umongo.fields.StringField()
    route = umongo.fields.ListField(umongo.fields.EmbeddedField(ProgressDocument))

    class Meta:
        collection_name = "application"


async def get(id_: entity.Id) -> Optional[Application]:
    got_document = await ApplicationDocument.find_one({"id_": id_})
    if got_document is None:
        return None
    return Application(
        id_=got_document.id_,
        applicant_id=got_document.applicant_id,
        workflow_id=got_document.workflow_id,
        route=[
            Progress(
                approver_id=progress.approver_id,
                approve=progress.approve,
                process_datetime=progress.process_datetime,
                comment=progress.comment,
            )
            for progress in got_document.route
        ],
    )


async def find() -> Generator[Application, None, None]:
    got_documents: Iterable[
        MotorAsyncIODocument
    ] = await ApplicationDocument.find().to_list(length=10)
    return (Application(**got_document.dump()) for got_document in got_documents)
