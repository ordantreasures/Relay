from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int]

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
