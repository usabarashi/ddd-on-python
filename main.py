import uvicorn
from fastapi import FastAPI

# Endpoints
import adapter.interface.auth.token
import adapter.interface.command.workflow.approval
import adapter.interface.query.application

app = FastAPI(title="DDD on Python")
app.include_router(router=adapter.interface.auth.token.router)
app.include_router(router=adapter.interface.command.workflow.approval.router)
app.include_router(router=adapter.interface.query.application.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
