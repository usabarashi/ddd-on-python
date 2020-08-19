"""Me
"""

from typing import Optional

from adapter.infrastructure.auth import account


async def browse_account(username: str) -> Optional[account.Account]:
    """アカウント情報を照会する
    """
    return await account.get(username=username)
