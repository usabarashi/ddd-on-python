"""Me
"""

from datetime import datetime
from dataclasses import asdict
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from adapter.infrastructure import mongodb
from adapter.infrastructure.auth import auth
from adapter.infrastructure.mongodb.dao import employee_dao
from query import account

router = APIRouter()


class ResponseAccount(BaseModel, employee_dao.Employee):
    id_: str
    username: str
    full_name: str
    email_address: str
    duties: List[int]
    join_date: Optional[datetime]
    retirement_date: Optional[datetime]
    hashed_password: str
    disabled: bool


@router.get(
    path="/query/me",
    tags=["query"],
    response_model=ResponseAccount,
    status_code=200,
    summary="",
    description="",
)
async def get_account(
    actor_id: str = Depends(auth.get_id),
):
    got_employee = await account.get_account(id_=mongodb.ULID(value=actor_id))
    if got_employee is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return ResponseAccount(**asdict(got_employee))
