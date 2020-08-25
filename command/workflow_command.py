from dataclasses import dataclass

from domain import application, entity, employee, workflow
from dsl.type import Err, Ok, Result


@dataclass
class WorkflowCommand:
    employee_repository: employee.Repository
    application_repository: application.Repository
    workflow_repository: workflow.Repository

    async def create(self, /, *, actor_id: entity.Id, workflow_id: entity.Id):
        """ワークフローを新規作成する"""
        raise NotImplementedError

    async def edit(self, /, *, actor_id: entity.Id, application_id: entity.Id):
        """ワークフローを編集する"""
        raise NotImplementedError

    async def delete(self, /, *, actor_id: entity.Id, application_id: entity.Id):
        """ワークフローを削除する"""
        raise NotImplementedError

    async def apply(self, /, *, actor_id: entity.Id):
        """申請する"""
        raise NotImplementedError

    async def approval(
        self, /, *, actor_id: entity.Id, application_id: entity.Id, comment: str
    ) -> Result[application.Error, application.Application]:
        """申請を承認する"""

        actor = await self.employee_repository.get(id_=actor_id)
        if actor is None:
            raise FileNotFoundError

        approve_application = await self.application_repository.get(id_=application_id)
        if approve_application is None:
            raise FileNotFoundError

        approve_workflow = await self.workflow_repository.get(
            id_=approve_application.workflow_id
        )
        if approve_workflow is None:
            raise FileNotFoundError

        result = actor.as_role(role=application.ApproverRole).approval(
            application=approve_application, workflow=approve_workflow, comment=comment,
        )
        if isinstance(result, Err):
            return Err(value=result.value)
        else:
            saved_application = await self.application_repository.save(
                entity=result.value
            )
            return Ok(value=saved_application)
