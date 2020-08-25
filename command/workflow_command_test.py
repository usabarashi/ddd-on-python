import asyncio
from typing import Optional

from command import workflow_command
from domain import application, entity, entity_test, employee, governance, workflow
from dsl.type import Err, Ok, ImmutableSequence


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

            class EmployeeRepositoryMock(employee.Repository):
                @staticmethod
                async def get(id_: int) -> Optional[employee.Employee]:
                    return employee.Employee(
                        id_=actor_id,
                        name="test_employee",
                        mail_address="test_mail_address",
                        duties=ImmutableSequence(
                            [governance.Duties.MANAGEMENT_DEPARTMENT]
                        ),
                        join_date=None,
                        retirement_date=None,
                    )

                @staticmethod
                async def save(entity: employee.Employee) -> employee.Employee:
                    return entity

            class ApplicationRepositoryMock(application.Repository):
                @staticmethod
                async def get(id_: int) -> Optional[application.Application]:
                    return application.Application(
                        id_=application_id,
                        applicant_id=applicant_id,
                        workflow_id=workflow_id,
                        route=application.Route(
                            [application.Progress(approver_id=actor_id)]),
                    )

                @staticmethod
                async def save(
                    entity: application.Application,
                ) -> application.Application:
                    return entity

            class WorkflowRepositoryMock(workflow.Repository):
                @staticmethod
                async def get(id_: entity.Id) -> Optional[workflow.Workflow]:
                    return workflow.Workflow(
                        id_=workflow_id,
                        name="test",
                        description="test",
                        duties=governance.Duties.MANAGEMENT_DEPARTMENT,
                    )

                @staticmethod
                async def save(entity: workflow.Workflow) -> workflow.Workflow:
                    return entity

            command = workflow_command.WorkflowCommand(
                employee_repository=EmployeeRepositoryMock(),
                application_repository=ApplicationRepositoryMock(),
                workflow_repository=WorkflowRepositoryMock(),
            )

            result = asyncio.run(
                command.approval(actor_id=actor_id,
                                 application_id=application_id, comment="test")
            )
            assert Ok is type(result)

    class Test異常系:
        @staticmethod
        def test_承認者が対象申請の管掌権限を持っていない場合はエラーとする():

            actor_id = entity_test.IdMock("actor_id")
            workflow_id = entity_test.IdMock("workflow_id")
            application_id = entity_test.IdMock("application_id")

            class EmployeeRepositoryMock(employee.Repository):
                @staticmethod
                async def get(id_: int) -> Optional[employee.Employee]:
                    return employee.Employee(
                        id_=actor_id,
                        name="test_employee",
                        mail_address="test_mail_address",
                        duties=ImmutableSequence([]),
                        join_date=None,
                        retirement_date=None,
                    )

                @staticmethod
                async def save(entity: employee.Employee) -> employee.Employee:
                    return entity

            class ApplicationRepositoryMock(application.Repository):
                @staticmethod
                async def get(id_: int) -> Optional[application.Application]:
                    return application.Application(
                        id_=application_id,
                        applicant_id=application_id,
                        workflow_id=workflow_id
                    )

                @staticmethod
                async def save(
                    entity: application.Application,
                ) -> application.Application:
                    return entity

            class WorkflowRepositoryMock(workflow.Repository):
                @staticmethod
                async def get(id_: entity.Id) -> Optional[workflow.Workflow]:
                    return workflow.Workflow(
                        id_=workflow_id,
                        name="test",
                        description="test",
                        duties=governance.Duties.MANAGEMENT_DEPARTMENT,
                    )

                @staticmethod
                async def save(entity: workflow.Workflow) -> workflow.Workflow:
                    return entity

            command = workflow_command.WorkflowCommand(
                employee_repository=EmployeeRepositoryMock(),
                application_repository=ApplicationRepositoryMock(),
                workflow_repository=WorkflowRepositoryMock(),
            )

            result = asyncio.run(
                command.approval(actor_id=actor_id,
                                 application_id=application_id, comment="test")
            )
            assert Err is type(result)
            assert isinstance(result.value, application.NoJobAuthorityError)
