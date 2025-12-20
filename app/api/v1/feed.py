# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/feed")
# async def get_feed():
#     return {"message": "Feed endpoint placeholder"}



from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.feed import get_feed_posts
from app.schemas.post import PostRead

router = APIRouter()

@router.get("/feed", response_model=list[PostRead])
async def feed(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db)):
    posts = await get_feed_posts(db, limit=limit, offset=offset)
    return posts
