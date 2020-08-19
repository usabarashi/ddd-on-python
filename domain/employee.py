from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, TypeVar

from domain import entity, governance
from dsl.type import ImmutableSequence

_S = TypeVar("_S")


@dataclass(eq=False, frozen=True)
class Employee(entity.Entity):
    """社員"""

    name: str
    mail_address: str
    duties: ImmutableSequence[governance.Duties] = field(
        default_factory=ImmutableSequence
    )
    join_date: Optional[datetime] = field(default=None)
    retirement_date: Optional[datetime] = field(default=None)
    id: entity.ID = field(default_factory=entity.generate_id)

    @property
    def is_enrolled(self: _S) -> bool:
        """在籍有無"""
        return (self.join_date is not None) and (self.retirement_date is None)

    def join(self: _S, account: str, mail_address: str, date: Optional[datetime]) -> _S:
        """入社する"""
        return self._update(
            account=account,
            mail_address=mail_address,
            join_date=date if date is not None else datetime.now().date,
        )

    def retire(self: _S, date: Optional[datetime]) -> _S:
        """退職する"""
        return self._update(
            retirement_date=date if date is not None else datetime.now().date
        )

    def assume_duties(self: _S, duties: governance.Duties) -> _S:
        """職務に就任する"""
        return self._update(duties=self.duties.append(duties))

    def leave_duties(self: _S, duties: governance.Duties) -> _S:
        """職務から離任する"""
        return self._update(duties=self.duties.remove(duties))


class Repository(ABC):
    @staticmethod
    @abstractmethod
    async def get(id: entity.ID) -> Optional[Employee]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def save(entity: Employee) -> Employee:
        raise NotImplementedError
