from fastapi import APIRouter

router = APIRouter()

@router.get("/query/application")
async def application():
    return {"Hello": "World"}