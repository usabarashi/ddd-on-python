"""Approval
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from adapter import interface
from adapter.infrastructure.mongodb.repository import repository_impl
from adapter.infrastructure.auth import auth
from adapter.infrastructure import mongodb
from command import workflow_command_test
from command.workflow_command import WorkflowCommand
from domain import application
from dsl.type import Err


router = APIRouter()
command = WorkflowCommand(repository=repository_impl.RepositoryImpl)


class Request(BaseModel):
    application_id: str
    comment: str = ""


class ResponseApplication(BaseModel, application.Application):
    id_: str
    applicant_id: str
    workflow_id: str
    route: application.Route

    class Config:
        arbitrary_types_allowed = True


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
async def approval(request: Request, actor_id: str = Depends(auth.get_id)):
    # Validation
    try:
        validated_actor_id = mongodb.ULID(actor_id)
        validated_application_id = mongodb.ULID(request.application_id)
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
