"""AcountDAO
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Generator, Iterable, List, Optional

import umongo
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument

from adapter.infrastructure import mongodb
from domain import entity


@dataclass(frozen=True)
class Employee:
    """DTO
    """
    id_: str 
    username: str
    full_name: str
    email_address: str
    duties: List[int]
    join_date: Optional[datetime]
    retirement_date: Optional[datetime]
    hashed_password: str
    disabled: bool


@mongodb.connector.register
class EmployeeDocument(MotorAsyncIODocument):
    id_ = umongo.fields.StringField(required=True, attribute="_id")
    username = umongo.fields.StringField()
    full_name = umongo.fields.StringField()
    email_address = umongo.fields.EmailField()
    duties = umongo.fields.ListField(umongo.fields.IntegerField())
    join_date = umongo.fields.DateTimeField(allow_none=True)
    retirement_date = umongo.fields.DateTimeField(allow_none=True)
    hashed_password = umongo.fields.StringField()
    disabled = umongo.fields.BooleanField()

    class Meta:
        collection_name = "employee"


async def get(id_: entity.Id) -> Optional[Employee]:
    got_document = await EmployeeDocument.find_one({"id_": id_})
    if got_document is None:
        return None
    return Employee(**got_document.dump())


async def find() -> Generator[Employee, None, None]:
    got_documents: Iterable[MotorAsyncIODocument] = await EmployeeDocument.find().to_list(length=10)
    return (Employee(**got_document.dump()) for got_document in got_documents)
