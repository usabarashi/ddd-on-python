import logging
from fastapi import FastAPI

from adapter.interface import commands, query


log = logging.getLogger(__name__)
app = FastAPI(title='DDD on Python')

app.include_router(commands.router)
app.include_router(query.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
