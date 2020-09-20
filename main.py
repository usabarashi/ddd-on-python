import uvicorn
from fastapi import FastAPI

import adapter.interface.auth.token
import adapter.interface.webapi.command.workflow.approval
import adapter.interface.webapi.query.me
from adapter import config

app = FastAPI(title=config["adapter"]["interface"]["webapi"]["APPLICATION_NAME"])
app.include_router(router=adapter.interface.auth.token.router)
app.include_router(router=adapter.interface.webapi.command.workflow.approval.router)
app.include_router(router=adapter.interface.webapi.query.me.router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config["adapter"]["interface"]["webapi"]["ALLOW_HOST"],
        port=config["adapter"]["interface"]["webapi"]["PORT"],
        reload=False,
    )
