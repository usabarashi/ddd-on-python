from fastapi import APIRouter

router = APIRouter()

@router.post("/commands/approval")
async def approval():
    return {"Hello": "World"}