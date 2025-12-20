from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    description: str
    category_id: int

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
