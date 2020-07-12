from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


import domain
from domain import employee, governance, workflow
from usecase import workflow_usecase
from dsl.type import ImmutableSequence

app = FastAPI()


class WorkflowApproveRequest(BaseModel):
    actor_id: int
    workflow_id: int
    comment: Optional[str] = None


class WorkflowApproveResponse(BaseModel, workflow.Workflow):
    pass


@app.post('/commands/workflow/approve', response_model=WorkflowApproveResponse)
async def workflow_approve(request: WorkflowApproveRequest) -> workflow.Workflow:

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

    result = await usecase.approve(
        actor_id=request.actor_id,
        workflow_id=request.workflow_id,
        comment=request.comment)
    return result.fold(
        err=lambda error: error,
        ok=lambda entity: entity.as_dict())


@app.get('/items/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
