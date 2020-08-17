"""Me
"""

from dataclasses import asdict

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from adapter.infrastructure.auth import account, auth

router = APIRouter()


@dataclass(frozen=True)
class ResponseAccount(BaseModel, account.Account):
    pass


@router.get(
    path="/me",
    tags=["query"],
    response_model=ResponseAccount,
    status_code=200,
    summary="",
    description="",
)
async def get_account(
    actor_account: account.Account = Depends(auth.get_account),
) -> ResponseAccount:
    return ResponseAccount(**asdict(actor_account))
