from typing import Optional, Tuple

from adapter.infrastructure import mongodb
from adapter.infrastructure.mongodb.dao import (
    application_dao,
    employee_dao,
    workflow_dao,
)
from domain import application, employee, entity, governance, repository, workflow
from dsl.type import ImmutableSequence


class RepositoryImpl(repository.Repository):
    @staticmethod
    async def get(
        employee_id: entity.Id, application_id: entity.Id
    ) -> Tuple[
        Optional[employee.Employee],
        Optional[application.Application],
        Optional[workflow.Workflow],
    ]:
        got_employee_dto = await employee_dao.get(id_=employee_id)
        got_employee = (
            None
            if got_employee_dto is None
            else employee.Employee(
                id_=mongodb.ULID(got_employee_dto.id_),
                username=got_employee_dto.username,
                full_name=got_employee_dto.full_name,
                email_address=got_employee_dto.email_address,
                hashed_password=got_employee_dto.hashed_password,
                duties=ImmutableSequence(
                    [governance.Duties(item) for item in got_employee_dto.duties]
                ),
                join_date=got_employee_dto.join_date,
                retirement_date=got_employee_dto.retirement_date,
                disabled=got_employee_dto.disabled,
            )
        )

        got_application_dto = await application_dao.get(id_=application_id)
        got_application = (
            None
            if got_application_dto is None
            else application.Application(
                id_=mongodb.ULID(got_application_dto.id_),
                applicant_id=mongodb.ULID(got_application_dto.applicant_id),
                workflow_id=mongodb.ULID(got_application_dto.workflow_id),
                route=application.Route(
                    [
                        application.Progress(
                            approver_id=mongodb.ULID(progress.approver_id),
                            approve=progress.approve,
                            process_datetime=progress.process_datetime,
                            comment=progress.comment,
                        )
                        for progress in got_application_dto.route
                    ]
                ),
            )
        )

        got_workflow_dto = await workflow_dao.get(id_=got_application.workflow_id)
        got_workflow = (
            None
            if got_workflow_dto is None
            else workflow.Workflow(
                id_=mongodb.ULID(got_workflow_dto.id_),
                name=got_workflow_dto.name,
                description=got_workflow_dto.description,
                duties=governance.Duties(got_workflow_dto.duties),
            )
        )

        return got_employee, got_application, got_workflow

    @staticmethod
    async def save(
        employee_entity: Optional[employee.Employee] = None,
        application_entity: Optional[application.Application] = None,
        workflow_entity: Optional[workflow.Workflow] = None,
    ) -> Tuple[
        Optional[employee.Employee],
        Optional[application.Application],
        Optional[workflow.Workflow],
    ]:
        # FIXME: Use ODM
        if employee_entity is not None:
            # await employee_dao.EmployeeDocument(**employee_entity.as_dict()).commit()
            employee_document = employee_entity.as_dict()
            employee_document.update({"_id": employee_document.pop("id_")})
            await mongodb.connector.db.employee.find_one_and_replace(
                filter={"_id": employee_document["_id"]},
                replacement=employee_document,
                upsert=True,
            )
        if application_entity is not None:
            # await application_dao.ApplicationDocument(**application_entity.as_dict()).commit()
            application_document = application_entity.as_dict()
            application_document.update({"_id": application_document.pop("id_")})
            await mongodb.connector.db.application.find_one_and_replace(
                filter={"_id": application_document["_id"]},
                replacement=application_document,
                upsert=True,
            )
        if workflow_entity is not None:
            # await workflow_dao.WorkflowDocument(**workflow_entity.as_dict()).commit()
            workflow_document = workflow_entity.as_dict()
            workflow_document.update({"_id": workflow_document.pop("id_")})
            await mongodb.connector.db.workflow.find_one_and_replace(
                filter={"_id": workflow_document["_id"]},
                replacement=workflow_entity,
                upsert=True,
            )

        return employee_entity, application_entity, workflow_entity
