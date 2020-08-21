from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from pydantic.dataclass import dataclass

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
    async def get(id: entity.ID) -> Optional[employee.Employee]:
        return employee.Employee(
            id=id,
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
    async def get(id: entity.ID) -> Optional[application.Application]:
        return application.Application(
            id=id,
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
            id=id,
            name="test",
            description="test",
            duties=governance.Duties.MANAGEMENT_DEPARTMENT,
        )

    @staticmethod
    async def save(entity: workflow.Workflow) -> workflow.Workflow:
        return entity


command = WorkflowCommand(
    employee_repository=EmployeeRepositoryMock(),
    application_repository=ApplicationRepositoryMock(),
    workflow_repository=WorkflowRepositoryMock(),
)


class Request(BaseModel):
    actor_id: str
    application_id: str
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

    # Validate request
    try:
        validated_actor_id = entity.ID(value=request.actor_id)
        validated_application_id = entity.ID(value=request.application_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    # Command
    result = await command.approval(
        actor_id=validated_actor_id,
        application_id=validated_application_id,
        comment=request.comment,
    )

    # Error handling
    if isinstance(result, Err):
        error = result.value
        if application.NoJobAuthorityError is type(error):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=error)
        if application.AlreadySottleError is type(error):
            raise HTTPException(status_code=status.HTTP_410_GONE, detail=error)
        if application.NotAnApproverError is type(error):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=error)
        if application.AlreayApproveError is type(error):
            raise HTTPException(
                status_code=status.HTTP_410_GONE, detail=error)
        # FIXME: Alert the system administrator
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Create resopnse
    else:
        return ResponseApplication(**result.value.as_dict())
