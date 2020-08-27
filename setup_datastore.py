"""Setup DataStore
"""
import asyncio
from datetime import datetime

from adapter.infrastructure import mongodb
from adapter.infrastructure.mongodb.dao import application_dao, employee_dao, workflow_dao
from domain import application, employee, governance, workflow
from dsl.type import ImmutableSequence

workflow_id = mongodb.ULID.generate()
employee_id = mongodb.ULID.generate()
application_id = mongodb.ULID.generate()


async def insert_workflow():
    entity = workflow.Workflow(
        id_=workflow_id,
        name="Sample",
        description="Sample",
        duties=governance.Duties.MANAGEMENT_DEPARTMENT,
    )
    await workflow_dao.WorkflowDocument(**entity.as_dict()).commit()


async def insert_user():
    entity = employee.Employee(
        id_=employee_id,
        username="johndoe",
        full_name="John Doe",
        email_address="johndoe@example.com",
        duties=ImmutableSequence(
            [governance.Duties.MANAGEMENT_DEPARTMENT]),
        join_date=datetime.now(),
        retirement_date=None,
        # plain_password="password",
        hashed_password="$2b$12$zfo4.zaRPiE4ArMukvG/.u4hHX1J0R3WKbIQLFliGqUURxthctyZ2",
        disabled=False,
    )
    await employee_dao.EmployeeDocument(**entity.as_dict()).commit()


async def insert_application():
    entity = application.Application(
        id_=application_id,
        applicant_id=employee_id,
        workflow_id=workflow_id,
        route=application.Route(
            [application.Progress(approver_id=employee_id)]),
    )
    await application_dao.ApplicationDocument(**entity.as_dict()).commit()

loop = asyncio.get_event_loop()
loop.run_until_complete(insert_workflow())
loop.run_until_complete(insert_user())
loop.run_until_complete(insert_application())
