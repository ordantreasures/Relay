# from fastapi import APIRouter

# router = APIRouter()

# @router.post("/auth/register")
# async def register():
#     return {"message": "Register placeholder"}

# @router.post("/auth/login")
# async def login():
#     return {"message": "Login placeholder"}


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.token import Token
from app.core.security import create_access_token

router = APIRouter()

@router.post("/auth/login", response_model=Token)
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    # TODO: validate user with DB
    # if invalid: raise HTTPException(status_code=401)
    user_id = 1  # placeholder
    token = create_access_token({"user_id": user_id})
    return {"access_token": token, "token_type": "bearer"}
