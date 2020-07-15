import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, Optional

import domain
from domain import employee, workflow
from dsl.type import Err, Ok, Result


@dataclass
class WorkflowUsecase:
    employee_repository: employee.Repository = employee.Repository
    workflow_repository: workflow.Repository = workflow.Repository

    async def approve(self, /, *, actor_id: domain.Id, workflow_id: domain.Id, comment: str) -> Awaitable[Result[workflow.Error, workflow.Workflow]]:
        """ワークフローを承認する"""

        actor = await self.employee_repository.get(id=actor_id)
        if actor is None:
            raise FileNotFoundError

        approve_workflow = await self.workflow_repository.get(id=workflow_id)
        if approve_workflow is None:
            raise FileNotFoundError

        approve_result = actor.as_role(role=workflow.ApproverRole).approval(
            workflow=approve_workflow,
            comment=comment)
        if type(approve_result) is Err:
            return approve_result
        approved_workflow: workflow.Workflow = approve_result.value

        saved_workflow = await self.workflow_repository.save(entity=approved_workflow)

        return Ok(saved_workflow)
