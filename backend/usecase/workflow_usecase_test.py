import asyncio
from typing import Optional
from typing import Awaitable

import domain
from domain import application, employee, governance, workflow
from dsl.type import Err, Ok, Result, ImmutableSequence
from usecase import workflow_usecase


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

            class EmployeeRepositoryMock(employee.Repository):
                @staticmethod
                async def get(id: int) -> Optional[employee.Employee]:
                    return employee.Employee(
                        id=1,
                        account="test_employee",
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
                async def get(id: int) -> Awaitable[Optional[application.Application]]:
                    return application.Application(
                        id=1,
                        applicant_id=1,
                        workflow_id=1,
                        route=application.Route([application.Progress(approver_id=1)]),
                    )

                @staticmethod
                async def save(
                    entity: application.Application,
                ) -> Awaitable[application.Application]:
                    return entity

            class WorkflowRepositoryMock(workflow.Repository):
                @staticmethod
                async def get(id: domain.Id) -> Optional[workflow.Workflow]:
                    return workflow.Workflow(
                        id=1,
                        name="test",
                        description="test",
                        duties=governance.Duties.MANAGEMENT_DEPARTMENT,
                    )

                @staticmethod
                async def save(entity: workflow.Workflow) -> workflow.Workflow:
                    return entity

            usecase = workflow_usecase.WorkflowUsecase(
                employee_repository=EmployeeRepositoryMock,
                application_repository=ApplicationRepositoryMock,
                workflow_repository=WorkflowRepositoryMock,
            )

            result = asyncio.run(
                usecase.approve(actor_id=1, application_id=1, comment="test")
            )
            assert Ok is type(result)

    class Test異常系:
        @staticmethod
        def test_承認者が対象申請の管掌権限を持っていない場合はエラーとする():
            class EmployeeRepositoryMock(employee.Repository):
                @staticmethod
                async def get(id: int) -> Optional[employee.Employee]:
                    return employee.Employee(
                        id=1,
                        account="test_employee",
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
                async def get(id: int) -> Awaitable[Optional[application.Application]]:
                    return application.Application(id=1, applicant_id=1,)

                @staticmethod
                async def save(
                    entity: application.Application,
                ) -> Awaitable[application.Application]:
                    return entity

            class WorkflowRepositoryMock(workflow.Repository):
                @staticmethod
                async def get(id: domain.Id) -> Optional[workflow.Workflow]:
                    return workflow.Workflow(
                        id=1,
                        name="test",
                        description="test",
                        duties=governance.Duties.MANAGEMENT_DEPARTMENT,
                    )

                @staticmethod
                async def save(entity: workflow.Workflow) -> workflow.Workflow:
                    return entity

            usecase = workflow_usecase.WorkflowUsecase(
                employee_repository=EmployeeRepositoryMock,
                application_repository=ApplicationRepositoryMock,
                workflow_repository=WorkflowRepositoryMock,
            )

            result = asyncio.run(
                usecase.approve(actor_id=1, application_id=1, comment="test")
            )
            assert Err is type(result)
            assert application.NoJobAuthorityError is type(result.value)
