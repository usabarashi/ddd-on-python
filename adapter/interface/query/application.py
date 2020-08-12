from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get(path="/query/application", tags=["query"])
async def application():
    return {"Hello": "World"}