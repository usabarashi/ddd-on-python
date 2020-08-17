"""Me
"""

from typing import Optional

from adapter.infrastructure.auth import account


async def browse_account(username: str) -> Optional[account.Account]:
    """アカウント情報を参照する
    """
    got_account = await account.get(username=username)

    if got_account is None:
        return None

    return got_account
