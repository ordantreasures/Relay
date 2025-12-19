from fastapi import APIRouter

router = APIRouter()

@router.get("/trending/posts")
async def trending_posts():
    return {"message": "Trending posts placeholder"}
