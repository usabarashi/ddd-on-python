from typing import Optional, Tuple

from adapter.infrastructure.mongodb.dao import employee_dao, application_dao, workflow_dao
from domain import application, employee, entity, repository, workflow


class WorkflowRepository(repository.Repository):

    @staticmethod
    async def get(
        employee_id: entity.Id,
        application_id: entity.Id
    ) -> Tuple[
        Optional[employee.Employee],
        Optional[application.Application],
        Optional[workflow.Workflow]
    ]:
        got_employee = await employee_dao.get(id_=employee_id)
        got_application = await application_dao.get(id_=application_id)
        got_workflow = await workflow_dao.get(id_=got_application.workflow_id)
        return got_employee, got_application, got_workflow

    @staticmethod
    async def save(
        employee_entity: employee.Employee,
        application_entity: application.Application,
        workflow_entity: workflow.Workflow,
    ) -> Tuple[
        employee.Employee,
        application.Application,
        workflow.Workflow
    ]:
        await employee_dao.EmployeeDocument(**employee_entity.as_dict()).commit()
        await application_dao.ApplicationDocument(**application_entity.as_dict()).commit()
        await workflow_dao.WorkflowDocument(**workflow_entity.as_dict()).commit()

        return employee_entity, application_entity, workflow_entity
