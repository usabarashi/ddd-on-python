"""Account
"""

from typing import Optional

from adapter.infrastructure.mongodb.dao import employee_dao
from domain import entity


async def get_account(id_: entity.Id) -> Optional[employee_dao.Employee]:
    """アカウント情報を照会する
    """
    got_account = await employee_dao.get(id_=id_)
    return got_account
