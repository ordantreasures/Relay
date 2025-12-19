from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/register")
async def register():
    return {"message": "Register placeholder"}

@router.post("/auth/login")
async def login():
    return {"message": "Login placeholder"}
