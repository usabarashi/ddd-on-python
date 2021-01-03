from dataclasses import dataclass
from enum import Enum
from typing import TypeVar

from dsl.type import Err, Ok

from domain import employee, entity, governance

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

    id_: entity.Id
    name: str
    description: str
    duties: governance.Duties = governance.Duties.MANAGEMENT_DEPARTMENT

    @classmethod
    def create_template(
        cls, id_: entity.Id, name: str, description: str, duties: governance.Duties
    ):
        """Factory method"""
        return cls(id_=id_, name=name, description=description, duties=duties)


class ManagerRole(employee.Employee):
    """部門管理者ロール"""

    def create(
        self,
        /,
        *,
        id_: entity.Id,
        name: str,
        description: str,
        duties: governance.Duties,
    ):
        """ワークフローを新規作成する"""

        if not name:
            return Err(NoNameError("名称が未定です."))
        if not description:
            return Err(NoDescriptionError("説明が未記入です."))
        if duties not in self.duties:
            return Err(NoJobAuthorityError("職務権限がありません."))

        return Ok(Workflow(id_=id_, name=name, description=description, duties=duties))

    def edit(self, /, *, workflow: Workflow, name=None, description=None, duties=None):
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
