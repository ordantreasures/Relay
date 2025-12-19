from fastapi import APIRouter

router = APIRouter()

@router.post("/posts/{post_id}/comments")
async def add_comment(post_id: int):
    return {"message": f"Add comment to post {post_id}"}
