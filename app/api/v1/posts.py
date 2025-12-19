from fastapi import APIRouter

router = APIRouter()

@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    return {"message": f"Get post {post_id}"}

@router.post("/posts")
async def create_post():
    return {"message": "Create post placeholder"}
