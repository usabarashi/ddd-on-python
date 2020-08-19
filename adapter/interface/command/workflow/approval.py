from dataclasses import dataclass
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from adapter import interface
from adapter.infrastructure.auth import account, auth
from domain import application, entity, employee, governance, workflow
from dsl.type import Err, ImmutableSequence
from command import workflow_command_test
from command.workflow_command import WorkflowCommand

router = APIRouter()

actor_id = entity.ID("01EG39KMDMRKVV70A2FAVVGBY9")
workflow_id = entity.ID("01EG3A4GBRDH3NZQVYZKRTQSJY")
application_id = entity.ID("01EG39Y1C2CKC5MAYJ68SBQ381")
applicant_id = entity.ID("01EG3A57EVTJFHTV2REY9J85M4")
approver_id = actor_id


class EmployeeRepositoryMock(employee.Repository):
    @staticmethod
    async def get(id: int) -> Optional[employee.Employee]:
        return employee.Employee(
            id=actor_id,
            name="test_employee",
            mail_address="test_mail_address",
            duties=ImmutableSequence(
                [governance.Duties.MANAGEMENT_DEPARTMENT]),
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
            id=application_id,
            applicant_id=applicant_id,
            workflow_id=workflow_id,
            route=application.Route(
                [application.Progress(approver_id=approver_id)]),
        )

    @staticmethod
    async def save(entity: application.Application,) -> application.Application:
        return entity


class WorkflowRepositoryMock(workflow.Repository):
    @staticmethod
    async def get(id: entity.ID) -> Optional[workflow.Workflow]:
        return workflow.Workflow(
            id=workflow_id,
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
    actor_id: entity.ID = entity.generate_id()
    application_id: entity.ID = entity.generate_id()
    comment: str = ""


@dataclass(eq=False, frozen=True)
class ResponseApplication(BaseModel, application.Application):
    pass


@router.put(
    path="/command/approval",
    tags=["command"],
    response_model=ResponseApplication,
    status_code=200,
    summary=command.approval.__doc__,
    description=interface.test_specification(module=workflow_command_test),
    responses={
        403: {"message": "NoJobAuthorityError"},
        410: {"message": "AlreadySottleError"},
    },
)
async def approval(request: Request, actor_account: account.Account = Depends(auth.get_account)):

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
        actor_id=entity.ID(request.actor_id),
        application_id=entity.ID(request.application_id),
        comment=request.comment,
    )
    if isinstance(result, Err):
        error_handling(error=result.value)
    else:
        return ResponseApplication(**result.value.as_dict())
