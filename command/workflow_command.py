from dataclasses import dataclass
from typing import Type, TypeVar

from domain import application, entity, repository
from dsl.type import Err, Ok

_T = TypeVar("_T")


@dataclass
class WorkflowCommand:
    repository: Type[repository.Repository]

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
    ):
        """申請を承認する"""

        actor, approve_application, approve_workflow = await self.repository.get(
            employee_id=actor_id, application_id=application_id
        )

        if actor is None or approve_application is None or approve_workflow is None:
            raise FileNotFoundError

        result = actor.as_role(role=application.ApproverRole).approval(
            application=approve_application, workflow=approve_workflow, comment=comment
        )

        if isinstance(result, Err):
            return Err(value=result.value)
        else:
            _, saved_application, _ = await self.repository.save(
                application_entity=result.value
            )
            return Ok(value=saved_application)
