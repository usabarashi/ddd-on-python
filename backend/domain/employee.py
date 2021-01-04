from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dsl.type import Vector

from domain import entity, governance


@dataclass(eq=False, frozen=True)
class Employee(entity.Entity):
    """社員"""

    id_: entity.Id
    username: str
    full_name: str
    email_address: str
    hashed_password: str
    duties: Vector[governance.Duties] = field(default_factory=Vector)
    join_date: Optional[datetime] = field(default=None)
    retirement_date: Optional[datetime] = field(default=None)
    disabled: bool = False

    @property
    def is_enrolled(self) -> bool:
        """在籍有無"""
        return (self.join_date is not None) and (self.retirement_date is None)

    def join(
        self, account: str, mail_address: str, date: Optional[datetime]
    ) -> Employee:
        """入社する"""
        return self._update(
            account=account,
            mail_address=mail_address,
            join_date=date if date is not None else datetime.now().date,
        )

    def retire(self, date: Optional[datetime]) -> Employee:
        """退職する"""
        return self._update(
            retirement_date=date if date is not None else datetime.now().date
        )

    def assume_duties(self, duties: governance.Duties) -> Employee:
        """職務に就任する"""
        return self._update(duties=self.duties.append(duties))

    def leave_duties(self, duties: governance.Duties) -> Employee:
        """職務から離任する"""
        return self._update(duties=self.duties.remove(duties))
