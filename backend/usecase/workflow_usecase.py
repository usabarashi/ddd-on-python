import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, Optional

import domain
from domain import application, employee, workflow
from dsl.type import Err, Ok, Result


@dataclass
class WorkflowUsecase:
    employee_repository: employee.Repository = employee.Repository
    application_repository: application.Repository = application.Repository
    workflow_repository: workflow.Repository = workflow.Repository

    async def create(self, /, *, actor_id: domain.Id, workflow_id: domain.Id):
        """ワークフローを新規作成する"""
        raise NotImplementedError

    async def edit(self, /, *, actor_id: domain.Id, application_id: domain.Id):
        """ワークフローを編集する"""
        raise NotImplementedError

    async def delete(self, /, *, actor_id: domain.Id, application_id: domain.Id):
        """ワークフローを削除する"""
        raise NotImplementedError

    async def apply(self, /, *, actor_id: domain.Id):
        """申請する"""
        raise NotImplementedError

    async def approve(
        self, /, *, actor_id: domain.Id, application_id: domain.Id, comment: str
    ) -> Awaitable[Result[application.Error, application.Application]]:
        """申請を承認する"""

        actor = await self.employee_repository.get(id=actor_id)
        if actor is None:
            raise FileNotFoundError
        approve_application = await self.application_repository.get(id=application_id)
        if approve_application is None:
            raise FileNotFoundError
        approve_workflow = await self.workflow_repository.get(
            id=approve_application.workflow_id
        )
        if approve_workflow is None:
            raise FileNotFoundError

        approve_result = actor.as_role(role=application.ApproverRole).approval(
            application=approve_application, workflow=approve_workflow, comment=comment
        )
        if type(approve_result) is Err:
            return approve_result
        approved_workflow: workflow.Workflow = approve_result.value

        saved_workflow = await self.workflow_repository.save(entity=approved_workflow)

        return Ok(saved_workflow)
