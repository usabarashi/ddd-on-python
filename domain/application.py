from abc import ABC, abstractmethod
from typing import Awaitable, Iterable, Optional, TypeVar
from enum import Enum
from datetime import datetime as _datetime
from dataclasses import field

import domain
from domain import employee, workflow
from dsl.type import ImmutableSequence, Err, Ok, Result

_S = TypeVar("_S")


class Judgment(Enum):
    APPROVED = 0
    REJECTED = 1


@domain.value
class Progress:
    """進捗"""

    approver_id: domain.Id = 0
    approve: Optional[Judgment] = field(default=None)
    datetime: Optional[_datetime] = field(default=None)
    comment: Optional[str] = field(default=None)


class Route(ImmutableSequence[Progress]):
    """承認経路"""

    def __init__(self, iterable: Iterable[Progress] = list()):
        ImmutableSequence.__init__(self, iterable)

    def is_complete(self) -> bool:
        """決済の有無"""
        return self.map(function=lambda process: process is Judgment.APPROVED).reduce(
            function=lambda left, right: left and right
        )

    def has_approver(self, approver: employee.Employee) -> bool:
        """承認者に含まれているか否か"""
        return self.filter(function=lambda process: process.approver_id == approver.id)

    def has_process(self, approver: employee.Employee) -> bool:
        """承認済みか否か"""
        return self.filter(
            function=lambda process: process.approver_id == approver.id
            and process.datetime is not None
        )

    def progress_approve(self, approver: employee.Employee, comment: str):
        """承認を追加する"""
        return Route(
            self.map(
                function=lambda progress: Progress(
                    approver_id=approver.id,
                    approve=True,
                    datetime=_datetime.now(),
                    comment=comment,
                )
                if progress.approver_id == approver.id
                else progress
            )
        )


@domain.entity
class Application(domain.Entity):
    id: Optional[domain.Id] = field(default_factory=None)
    applicant_id: domain.Id = 0
    workflow_id: domain.Id = 0
    route: Route = field(default_factory=Route)

    def process(self: _S, approver: employee.Employee, comment: str) -> _S:
        """処理する"""
        return self._update(
            route=self.route.progress_approve(approver=approver, comment=comment)
        )


class Repository(ABC):
    """リポジトリ"""

    @staticmethod
    @abstractmethod
    async def get(id: domain.Id) -> Awaitable[Optional[Application]]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def save(entity: Application) -> Awaitable[Application]:
        raise NotImplementedError


class Error(domain.Error):
    """申請エラー"""

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

    def has_process(self, application: Application):
        """処理の有無"""
        if application.duties not in self.duties:
            return False
        if application.route.is_complete:
            return False
        if not application.route.has_approver(approver=self):
            return False

        if application.route.has_process(approver=self):
            return True

    def approval(
        self: _S, application: Application, workflow: workflow.Workflow, comment: str
    ) -> Result[domain.Error, Application]:
        """承認する"""
        if workflow.duties not in self.duties:
            return Err(NoJobAuthorityError("職務権限がありません."))

        if application.route.is_complete():
            return Err(AlreadySottleError("決裁済みです."))

        if not application.route.has_approver(approver=self):
            return Err(NotAnApproverError("承認経路に含まれていません."))

        if application.route.has_process(approver=self):
            return Err(AlreayApproveError("承認済みです."))

        return Ok(application.process(approver=self, comment=comment))

