"""Account
"""

from typing import Optional

from adapter.infrastructure import mongodb
from adapter.infrastructure.mongodb.dao import employee_dao


async def get_account(id_: mongodb.ULID) -> Optional[employee_dao.Employee]:
    """アカウント情報を照会する
    """
    got_account = await employee_dao.get(id_=id_)
    return got_account
