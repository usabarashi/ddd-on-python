from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import List, Optional, TypeVar

from dsl.type import Err, Ok, Result, Vector

import domain
from domain import employee, entity, workflow

_S = TypeVar("_S")


class Judgment(IntEnum):
    APPROVED = 0
    REJECTED = 1


@dataclass(eq=False, frozen=True)
class Progress:
    """進捗"""

    approver_id: entity.Id
    approve: Optional[Judgment] = field(default=None)
    process_datetime: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)


class Route(Vector[Progress]):
    """承認経路"""

    def __init__(self, sequence: List[Progress] = None):
        if sequence is None:
            sequence = []
        Vector.__init__(self, sequence)

    def is_complete(self) -> bool:
        """決済の有無"""
        return self.map(
            function=lambda progress: progress.approve is Judgment.APPROVED
        ).reduce(function=lambda left, right: left and right)

    def has_approver(self, approver: employee.Employee) -> bool:
        """承認者に含まれているか否か"""
        return (
            0
            < self.filter(
                function=lambda process: process.approver_id == approver.id_
            ).size()
        )

    def has_process(self, approver: employee.Employee) -> bool:
        """承認済みか否か"""
        return (
            0
            < self.filter(
                function=lambda process: process.approver_id == approver.id_
                and process.process_datetime is not None
            ).size()
        )

    def progress_approve(self, approver: employee.Employee, comment: str):
        """承認を追加する"""
        return self.map(
            function=lambda progress: Progress(
                approver_id=approver.id_,
                approve=Judgment.APPROVED,
                process_datetime=datetime.now(),
                comment=comment,
            )
            if progress.approver_id == approver.id_
            else progress
        )


@dataclass(eq=False, frozen=True)
class Application(entity.Entity):
    id_: entity.Id
    applicant_id: entity.Id
    workflow_id: entity.Id
    route: Route = field(default_factory=Route)

    def process(self, approver: employee.Employee, comment: str):
        """処理する"""
        return self._update(
            route=self.route.progress_approve(approver=approver, comment=comment)
        )


class Error(domain.Error):
    """申請エラー"""


class NoJobAuthorityError(Error):
    """職務権限なしエラー"""


class AlreadySottleError(Error):
    """決済済エラー"""


class NotAnApproverError(Error):
    """承認経路に含まれていないエラー"""


class AlreayApproveError(Error):
    """承認済みエラー"""


@dataclass(eq=False, frozen=True)
class ApproverRole(employee.Employee):
    """承認者ロール"""

    def has_process(self, application: Application, workflow: workflow.Workflow):
        """処理の有無"""
        if workflow.duties not in self.duties:
            return False
        if application.route.is_complete():
            return False
        if not application.route.has_approver(approver=self):
            return False

        if application.route.has_process(approver=self):
            return True

    def approval(
        self, application: Application, workflow: workflow.Workflow, comment: str
    ) -> Result[Error, Application]:
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
