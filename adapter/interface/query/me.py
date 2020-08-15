# -*- coding: utf-8 -*-
"""Me
"""

from dataclasses import asdict

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from adapter.infrastructure.auth import auth
from adapter.infrastructure.auth.account_dao import Account

router = APIRouter()


@dataclass(eq=False, frozen=True)
class ResponseAccount(BaseModel, Account):
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
    actor_account: Account = Depends(auth.get_account),
) -> ResponseAccount:
    return ResponseAccount(**asdict(actor_account))
