from abc import abstractclassmethod
from typing import Optional, Tuple

from domain import application, employee, entity, workflow


class Repository:

    @staticmethod
    @abstractclassmethod
    async def get(
        employee_id: entity.Id,
        application_id: entity.Id
    ) -> Tuple[
            Optional[employee.Employee],
            Optional[application.Application],
            Optional[workflow.Workflow]
    ]:
        raise NotImplementedError

    @staticmethod
    @abstractclassmethod
    async def save(
        employee_entity: entity.Entity,
        application_entity: entity.Entity,
        workflow_entity: entity.Entity
    ) -> Tuple[employee.Employee, application.Application, workflow.Workflow]:
        raise NotImplementedError
