from abc import ABC, abstractmethod
from typing import Awaitable, Iterable, Optional, TypeVar
from enum import Enum
from datetime import datetime
from dataclasses import field

import domain
from domain import employee, governance
from dsl.type import ImmutableSequence, Err, Ok, Result


_S = TypeVar('_S')


class Procedure(Enum):
    """ワークフロー種別"""
    JOINING = 0
    RETIREMENT = 1


@domain.value
class Process:
    """進捗"""
    approver_id: domain.Id
    approve: bool = False
    datetime: Optional[datetime] = None
    comment: Optional[str] = None

    @property
    def is_processed(self):
        """処理の有無"""
        return self.datetime is not None


class Route(ImmutableSequence[Process]):
    """承認経路"""

    def __init__(self, iterable: Iterable[Process] = list()):
        ImmutableSequence.__init__(self, iterable)

    @property
    def is_complete(self) -> bool:
        """決済の有無"""
        return self.map(
            function=lambda process: process.is_processed
        ).reduce(
            function=lambda left, right: left and right)

    def has_approver(self, approver: employee.Employee) -> bool:
        """承認者に含まれているか否か"""
        return self.filter(function=lambda process: process.approver_id == approver.id)

    def has_process(self, approver: employee.Employee) -> bool:
        """承認済みか否か"""
        return self.filter(
            function=lambda process:
            process.approver_id == approver.id and
            process.datetime is not None)

    def progress_approve(self, approver: employee.Employee, comment: str):
        """承認を追加する"""
        return Route(self.map(
            function=lambda process: Process(approver_id=approver.id,
                                             approve=True,
                                             datetime=datetime.now(),
                                             comment=comment)
            if process.approver_id == approver.id
            else process
        ))


@ domain.entity
class Workflow(domain.Entity):
    """ワークフロー"""
    id: Optional[domain.Id] = field(default_factory=None)
    duties: governance.Duties = governance.Duties.MANAGEMENT_DEPARTMENT
    procedure: Procedure = Procedure.JOINING
    applicant_id: domain.Id = 0
    route: Route = field(default_factory=Route)

    def process(self: _S, approver: employee.Employee, comment: str) -> _S:
        return self._update(
            route=self.route.progress_approve(
                approver=approver, comment=comment)
        )

    @staticmethod
    def create_template() -> _S:
        """Factory method"""
        return Workflow()


class Repository(ABC):
    """ワークフローリポジトリ"""

    @classmethod
    @abstractmethod
    async def get(id: int) -> Awaitable[Optional[Workflow]]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def save(entity: Workflow) -> Awaitable[Workflow]:
        raise NotImplementedError


class Error(domain.Error):
    """ワークフローエラー"""
    pass


class NoJobAuthorityError(Error):
    """職務権限なしエラー"""
    pass


class AlreadySottleError(Error):
    """決済済エラー"""
    pass


class NotAnApproverError(Error):
    """承認経路に含まれていないエラー"""
    pass


class AlreayApproveError(Error):
    """承認済みエラー"""
    pass


@domain.entity
class ApproverRole(employee.Employee):
    """承認者ロール"""

    def approval(self:  _S, workflow: Workflow, comment: str) -> Result[domain.Error, Workflow]:
        """承認する"""
        if workflow.duties not in self.duties:
            return Err(NoJobAuthorityError('職務権限がありません.'))

        if workflow.route.is_complete:
            return Err(AlreadySottleError('決裁済みです.'))

        if not workflow.route.has_approver(approver=self):
            return Err(NotAnApproverError('承認経路に含まれていません.'))

        if workflow.route.has_process(approver=self):
            return Err(AlreayApproveError('承認済みです.'))

        return Ok(workflow.process(approver=self, comment=comment))
