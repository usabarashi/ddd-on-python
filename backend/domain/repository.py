from abc import ABC, abstractclassmethod
from typing import Optional, Tuple

from domain import application, employee, entity, workflow


class Repository(ABC):
    @staticmethod
    @abstractclassmethod
    async def get(
        employee_id: entity.Id, application_id: entity.Id
    ) -> Tuple[
        Optional[employee.Employee],
        Optional[application.Application],
        Optional[workflow.Workflow],
    ]:
        raise NotImplementedError

    @staticmethod
    @abstractclassmethod
    async def save(
        employee_entity: Optional[employee.Employee] = None,
        application_entity: Optional[application.Application] = None,
        workflow_entity: Optional[workflow.Workflow] = None,
    ) -> Tuple[
        Optional[employee.Employee],
        Optional[application.Application],
        Optional[workflow.Workflow],
    ]:
        raise NotImplementedError
