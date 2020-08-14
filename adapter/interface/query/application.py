from fastapi import APIRouter

router = APIRouter()


@router.get(path="/query/application", tags=["query"])
async def application() -> dict:
    return {"Hello": "World"}
