"""Account

EmployeeCollectionを参照して認証に必要なAccount情報だけ取得する.
"""

from dataclasses import dataclass
from typing import Optional

from adapter.infrastructure.mongodb.dao import employee_dao


@dataclass(frozen=True)
class Account:
    """DTO
    """

    id_: str
    username: str
    hashed_password: str


async def get(id_: str) -> Optional[Account]:
    """アクティブアカウントを取得する
    """
    got_document = await employee_dao.EmployeeDocument.find_one(
        filter={"_id": id_, "disabled": False}
    )

    if got_document is None:
        return None

    got_employee = employee_dao.Employee(**got_document.dump())
    return Account(
        id_=str(got_employee.id_),
        username=got_employee.username,
        hashed_password=got_employee.hashed_password,
    )


async def find(username: str) -> Optional[Account]:
    """アクティブアカウントを取得する
    """
    got_document = await employee_dao.EmployeeDocument.find_one(
        filter={"username": username, "disabled": False}
    )

    if got_document is None:
        return None

    got_employee = employee_dao.Employee(**got_document.dump())
    return Account(
        id_=str(got_employee.id_),
        username=got_employee.username,
        hashed_password=got_employee.hashed_password,
    )
