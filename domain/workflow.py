from abc import ABC, abstractmethod
from typing import Optional, TypeVar
from enum import Enum
from dataclasses import dataclass, field

import domain
from domain import entity, employee, governance
from dsl.type import Err, Ok, Result


_S = TypeVar("_S")


class Procedure(Enum):
    """ワークフロー種別"""

    JOINING = 0
    RETIREMENT = 1


class Error(Exception):
    """ワークフローエラー"""


class NoNameError(Error):
    """名称未定義エラー"""


class NoDescriptionError(Error):
    """説明未記載エラー"""


class NoJobAuthorityError(Error):
    """承認権限エラー"""


@dataclass(eq=False, frozen=True)
class Workflow(entity.Entity):
    """ワークフロー"""

    name: str
    description: str
    duties: governance.Duties = governance.Duties.MANAGEMENT_DEPARTMENT
    id: entity.ID = field(default_factory=entity.generate_id)

    @staticmethod
    def create_template(name: str, description: str, duties: governance.Duties) -> _S:
        """Factory method"""
        return Workflow(name=name, description=description, duties=duties)


class Repository(ABC):
    @staticmethod
    @abstractmethod
    async def get(id: entity.ID) -> Optional[Workflow]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def save(entity: Workflow) -> Workflow:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def remove(entity: Workflow) -> Workflow:
        raise NotImplementedError


class ManagerRole(employee.Employee):
    """部門管理者ロール"""

    def create(
        self, /, *, name: str, description: str, duties: governance.Duties
    ) -> Result[domain.Error, Workflow]:
        """ワークフローを新規作成する"""

        if not name:
            return Err(NoNameError("名称が未定です."))
        if not description:
            return Err(NoDescriptionError("説明が未記入です."))
        if duties not in self.duties:
            return Err(NoJobAuthorityError("職務権限がありません."))

        return Ok(Workflow(name=name, description=description, duties=duties))

    def edit(
        self, /, *, workflow: Workflow, name=None, description=None, duties=None
    ) -> Result[Error, Workflow]:
        """ワークフローを編集する
        FIXME: 申請済がある場合はどうする？
        """

        if not name:
            return Err(NoNameError("名称が未定です."))
        if not description:
            return Err(NoDescriptionError("説明が未記入です."))
        if (not duties) and (duties not in self.duties):
            return Err(NoJobAuthorityError("職務権限がありません."))

        return Ok(
            workflow._update(
                name=name if name else workflow.name,
                description=description if description else description,
                duties=duties if duties else duties,
            )
        )
