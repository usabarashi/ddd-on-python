from abc import ABC, abstractclassmethod
from dataclasses import field
from datetime import datetime
from typing import Awaitable, Optional, TypeVar

import domain
from domain import governance
from dsl.type import ImmutableSequence

_S = TypeVar('_S')


@domain.entity
class Employee(domain.Entity):
    """社員"""
    id: Optional[domain.Id] = field(default_factory=None)
    account: str = field(default='')
    name: str = field(default='')
    mail_address: str = field(default='')
    duties: ImmutableSequence[governance.Duties] = field(
        default_factory=ImmutableSequence)
    join_date: Optional[datetime.date] = field(default_factory=None)
    retirement_date: Optional[datetime.date] = field(default_factory=None)

    @property
    def is_enrolled(self: _S) -> bool:
        """在籍有無"""
        return (self.join_date is not None) and (self.retirement_date is None)

    def join(self: _S, account: str, mail_address: str, date: Optional[datetime.date]) -> _S:
        """入社する"""
        return self._update(
            account=account,
            mail_address=mail_address,
            join_date=date if date is not None else datetime.now().date
        )

    def retire(self: _S, date: Optional[datetime.date]) -> _S:
        """退職する"""
        return self._update(retirement_date=date if date is not None else datetime.now().date)

    def assume_duties(self: _S, duties: governance.Duties) -> _S:
        """職務に就任する"""
        return self._update(duties=self.duties.append(duties))

    def leave_duties(self: _S, duties: governance.Duties) -> _S:
        """職務から離任する"""
        return self._update(duties=self.duties.remove(duties))


class Repository(ABC):
    """Repository"""

    @staticmethod
    @abstractclassmethod
    async def get(id_: domain.Id) -> Awaitable[Optional[Employee]]:
        """get"""
        raise NotImplementedError

    @staticmethod
    @abstractclassmethod
    async def save(entity: Employee) -> Awaitable[Employee]:
        """save"""
        raise NotImplementedError
