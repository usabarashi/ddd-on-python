# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI

# Auth endpoints
import adapter.interface.auth.token

# Command endpoint
import adapter.interface.command.workflow.approval

# Query endpoint
import adapter.interface.query.application
import adapter.interface.query.me

app = FastAPI(title="DDD on Python")
# Auth
app.include_router(router=adapter.interface.auth.token.router)
# Command
app.include_router(router=adapter.interface.command.workflow.approval.router)
# Query
app.include_router(router=adapter.interface.query.application.router)
app.include_router(router=adapter.interface.query.me.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
