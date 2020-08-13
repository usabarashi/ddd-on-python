from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import domain
from adapter import interface
from domain import application, employee, governance, workflow
from dsl.type import ImmutableSequence
from command import workflow_command_test
from command.workflow_command import WorkflowCommand

router = APIRouter()


class EmployeeRepositoryMock(employee.Repository):
    @staticmethod
    async def get(id: int) -> Optional[employee.Employee]:
        return employee.Employee(
            id=1,
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
    async def get(id: int) -> Optional[application.Application]:
        return application.Application(
            id=1,
            applicant_id=1,
            workflow_id=1,
            route=application.Route([application.Progress(approver_id=1)]),
        )

    @staticmethod
    async def save(entity: application.Application,) -> application.Application:
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


command = WorkflowCommand(
    employee_repository=EmployeeRepositoryMock,
    application_repository=ApplicationRepositoryMock,
    workflow_repository=WorkflowRepositoryMock,
)


class Request(BaseModel):
    actor_id: int = 0
    application_id: int = 0
    comment: str = ""


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
async def approval(request: Request):
    def error_handling(error: application.Error):
        if application.NoJobAuthorityError is type(error):
            raise HTTPException(status_code=403, detail=error.message)
        elif application.AlreadySottleError is type(error):
            raise HTTPException(status_code=410, detail=error.message)
        elif application.NotAnApproverError is type(error):
            raise HTTPException(status_code=403, detail=error.message)
        elif application.AlreayApproveError is type(error):
            raise HTTPException(status_code=403, detail=error.message)
        else:
            raise HTTPException(status_code=500)

    result = await command.approval(
        actor_id=request.actor_id,
        application_id=request.application_id,
        comment=request.comment,
    )
    return result.fold(
        err=lambda error: error_handling(error=error),
        ok=lambda result: result.as_dict(),
    )
