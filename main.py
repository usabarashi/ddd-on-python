import uvicorn
from fastapi import FastAPI

# Endpoints
from adapter.interface.commands import approval as commands_approval
from adapter.interface.query import application as query_application

app = FastAPI()
app.include_router(router=commands_approval.router)
app.include_router(router=query_application.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)