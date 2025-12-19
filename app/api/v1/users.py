from fastapi import APIRouter

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"message": f"Get user {user_id}"}
