import asyncio
from typing import Optional, Tuple

from command import workflow_command
from domain import (
    application,
    employee,
    entity,
    entity_test,
    governance,
    repository,
    workflow,
)
from dsl.type import Err, ImmutableSequence, Ok


class Test承認:
    class Test正常系:
        @staticmethod
        def test_承認する():
            """アクターが下記条件を満たす場合, 対象の申請を承認する.
            - アクターが申請に対する職務権限をもっている.
            - 申請が決裁されていない.
            - 申請の承認経路にアクターが含まれている.
            - 申請に対してアクターが承認/差戻し/却下をおこなっていない.
            """

            actor_id = entity_test.IdMock("actor_id")
            workflow_id = entity_test.IdMock("workflow_id")
            application_id = entity_test.IdMock("application_id")
            applicant_id = entity_test.IdMock("applicant_id")

            class RepositoryMock(repository.Repository):
                @staticmethod
                async def get(
                    employee_id: entity.Id, application_id: entity.Id
                ) -> Tuple[
                    Optional[employee.Employee],
                    Optional[application.Application],
                    Optional[workflow.Workflow],
                ]:
                    employee_entity = employee.Employee(
                        id_=employee_id,
                        username="test",
                        full_name="test",
                        email_address="test",
                        duties=ImmutableSequence(
                            [governance.Duties.MANAGEMENT_DEPARTMENT]
                        ),
                        join_date=None,
                        retirement_date=None,
                        hashed_password="",
                        disabled=False,
                    )

                    application_entity = application.Application(
                        id_=application_id,
                        applicant_id=applicant_id,
                        workflow_id=workflow_id,
                        route=application.Route(
                            [application.Progress(approver_id=actor_id)]
                        ),
                    )

                    workflow_entity = workflow.Workflow(
                        id_=workflow_id,
                        name="test",
                        description="test",
                        duties=governance.Duties.MANAGEMENT_DEPARTMENT,
                    )

                    return employee_entity, application_entity, workflow_entity

                @staticmethod
                async def save(
                    employee_entity: employee.Employee = None,
                    application_entity: application.Application = None,
                    workflow_entity: workflow.Workflow = None,
                ) -> Tuple[
                    Optional[employee.Employee],
                    Optional[application.Application],
                    Optional[workflow.Workflow],
                ]:
                    return employee_entity, application_entity, workflow_entity

            command = workflow_command.WorkflowCommand(repository=RepositoryMock)

            result = asyncio.run(
                command.approval(
                    actor_id=actor_id, application_id=application_id, comment="test"
                )
            )
            assert Ok is type(result)

    class Test異常系:
        @staticmethod
        def test_承認者が対象申請の管掌権限を持っていない場合はエラーとする():

            actor_id = entity_test.IdMock("actor_id")
            workflow_id = entity_test.IdMock("workflow_id")
            application_id = entity_test.IdMock("application_id")

            class RepositoryMock(repository.Repository):
                @staticmethod
                async def get(
                    employee_id: entity.Id, application_id: entity.Id
                ) -> Tuple[
                    Optional[employee.Employee],
                    Optional[application.Application],
                    Optional[workflow.Workflow],
                ]:
                    employee_entity = employee.Employee(
                        id_=employee_id,
                        username="test_employee",
                        full_name="test",
                        email_address="test_mail_address",
                        duties=ImmutableSequence([]),
                        join_date=None,
                        retirement_date=None,
                        hashed_password="",
                        disabled=False,
                    )

                    application_entity = application.Application(
                        id_=application_id,
                        applicant_id=application_id,
                        workflow_id=workflow_id,
                    )

                    workflow_entity = workflow.Workflow(
                        id_=workflow_id,
                        name="test",
                        description="test",
                        duties=governance.Duties.MANAGEMENT_DEPARTMENT,
                    )

                    return employee_entity, application_entity, workflow_entity

                @staticmethod
                async def save(
                    employee_entity: employee.Employee = None,
                    application_entity: application.Application = None,
                    workflow_entity: workflow.Workflow = None,
                ) -> Tuple[
                    Optional[employee.Employee],
                    Optional[application.Application],
                    Optional[workflow.Workflow],
                ]:
                    return employee_entity, application_entity, workflow_entity

            command = workflow_command.WorkflowCommand(repository=RepositoryMock)

            result = asyncio.run(
                command.approval(
                    actor_id=actor_id, application_id=application_id, comment="test"
                )
            )
            assert Err is type(result)
            assert isinstance(result.value, application.NoJobAuthorityError)
