import asyncio
from typing import Optional

import domain
from domain import employee, governance, workflow
from dsl.type import Err, Ok, Result, ImmutableSequence
from usecase import workflow_usecase
import asyncio


def test_approve():
    """
    アクターが下記条件を満たす場合, 対象の申請を承認する.
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
                account='test_employee',
                name='test_employee',
                mail_address='test_mail_address',
                duties=ImmutableSequence([
                        governance.Duties.MANAGEMENT_DEPARTMENT
                ]),
                join_date=None,
                retirement_date=None
            )

        @ staticmethod
        async def save(entity: employee.Employee) -> employee.Employee:
            return entity

    class WorkflowRepositoryMock(workflow.Repository):

        @staticmethod
        async def get(id: domain.Id) -> Optional[workflow.Workflow]:
            return workflow.Workflow(
                id=1,
                duties=governance.Duties.MANAGEMENT_DEPARTMENT,
                procedure=workflow.Procedure.JOINING,
                applicant_id=1,
                route=workflow.Route([
                    workflow.Process(
                        approver_id=1,
                        approve=False,
                        datetime=None,
                        comment=None
                    )]
                )
            )

        @staticmethod
        async def save(entity: workflow.Workflow) -> workflow.Workflow:
            return entity

    usecase = workflow_usecase.WorkflowUsecase(
        employee_repository=EmployeeRepositoryMock,
        workflow_repository=WorkflowRepositoryMock)

    result = asyncio.run(usecase.approve(
        actor_id=1, workflow_id=1, comment='test'))
    assert Ok is type(result)


def test_no_job_authority():
    """
    アクターが対象申請に対する職務権限を持っていない場合, エラーとする.
    """

    class EmployeeRepositoryMock(employee.Repository):

        @staticmethod
        async def get(id: int) -> Optional[employee.Employee]:
            return employee.Employee(
                id=1,
                account='test_employee',
                name='test_employee',
                mail_address='test_mail_address',
                duties=ImmutableSequence([]),
                join_date=None,
                retirement_date=None
            )

        @staticmethod
        async def save(entity: employee.Employee) -> employee.Employee:
            return entity

    class WorkflowRepositoryMock(workflow.Repository):

        @staticmethod
        async def get(id: domain.Id) -> Optional[workflow.Workflow]:
            return workflow.Workflow(
                id=1,
                duties=governance.Duties.MANAGEMENT_DEPARTMENT,
                procedure=workflow.Procedure.JOINING,
                applicant_id=1,
                route=workflow.Route([
                    workflow.Process(
                        approver_id=1,
                        approve=False,
                        datetime=None,
                        comment=None
                    )]
                )
            )

        @staticmethod
        async def save(entity: workflow.Workflow) -> workflow.Workflow:
            return entity

    usecase = workflow_usecase.WorkflowUsecase(
        employee_repository=EmployeeRepositoryMock,
        workflow_repository=WorkflowRepositoryMock)

    result = asyncio.run(usecase.approve(
        actor_id=1, workflow_id=1, comment='test'))
    assert Err == type(result)
    assert workflow.NoJobAuthorityError == type(result.value)
