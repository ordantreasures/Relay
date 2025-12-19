from fastapi import APIRouter

router = APIRouter()

@router.get("/categories")
async def list_categories():
    return {"message": "List all categories"}
