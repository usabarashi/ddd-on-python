from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

import domain
from adapter import interface
from adapter.infrastructure.auth import auth
from adapter.infrastructure.auth.account_dao import Account
from domain import application, employee, governance, workflow
from dsl.type import Err, ImmutableSequence
from command import workflow_command_test
from command.workflow_command import WorkflowCommand

router = APIRouter()


class EmployeeRepositoryMock(employee.Repository):
    @staticmethod
    async def get(id_: int) -> Optional[employee.Employee]:
        return employee.Employee(
            id_=1,
            account="test_employee",
            name="test_employee",
            mail_address="test_mail_address",
            duties=ImmutableSequence([governance.Duties.MANAGEMENT_DEPARTMENT]),
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
            id_=1,
            applicant_id=1,
            workflow_id=1,
            route=application.Route([application.Progress(approver_id=1)]),
        )

    @staticmethod
    async def save(entity: application.Application,) -> application.Application:
        return entity


class WorkflowRepositoryMock(workflow.Repository):
    @staticmethod
    async def get(id_: domain.Id) -> Optional[workflow.Workflow]:
        return workflow.Workflow(
            id_=1,
            name="test",
            description="test",
            duties=governance.Duties.MANAGEMENT_DEPARTMENT,
        )

    @staticmethod
    async def save(entity: workflow.Workflow) -> workflow.Workflow:
        return entity


command = WorkflowCommand(
    employee_repository=EmployeeRepositoryMock,
    application_repository=ApplicationRepositoryMock,
    workflow_repository=WorkflowRepositoryMock,
)


class Request(BaseModel):
    actor_id: int = 0
    application_id: int = 0
    comment: str = ""


@dataclass(eq=False, frozen=True)
class ResponseApplication(BaseModel, application.Application):
    pass


@router.put(
    path="/commands/approval",
    tags=["command"],
    # response_model=application.Application,
    status_code=200,
    summary=command.approval.__doc__,
    description=interface.test_specification(module=workflow_command_test),
    responses={
        403: {"message": "NoJobAuthorityError"},
        410: {"message": "AlreadySottleError"},
    },
)
async def approval(
    request: Request, actor_account: Account = Depends(auth.get_account)
) -> ResponseApplication:
    def error_handling(error: application.Error):
        if application.NoJobAuthorityError is type(error):
            raise HTTPException(status_code=403, detail=error)
        if application.AlreadySottleError is type(error):
            raise HTTPException(status_code=410, detail=error)
        if application.NotAnApproverError is type(error):
            raise HTTPException(status_code=403, detail=error)
        if application.AlreayApproveError is type(error):
            raise HTTPException(status_code=403, detail=error)
        raise HTTPException(status_code=500)

    result = await command.approval(
        actor_id=request.actor_id,
        application_id=request.application_id,
        comment=request.comment,
    )
    if isinstance(result, Err):
        error_handling(error=result.value)
    else:
        return ResponseApplication(**result.value.as_dict())
