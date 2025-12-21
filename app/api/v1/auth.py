from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserLogin, UserCreate
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.rate_limit import rate_limit
from datetime import timedelta

router = APIRouter()

@router.post("/auth/login", response_model=Token)
@rate_limit(max_requests=5, time_window=60)  # 5 attempts per minute
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    # Check user exists
    stmt = select(User).where(User.email == login_data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.hashed_password.value):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    # Create token
    token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=timedelta(hours=24)
    )
    
    return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/register")
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check if user exists
    stmt = select(User).where(
        (User.email == user_data.email) | (User.username == user_data.username)
    )
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "created_at": new_user.created_at
    }