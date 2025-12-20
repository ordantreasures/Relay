from pydantic import BaseModel
from datetime import datetime

class EngagementBase(BaseModel):
    type: str  # like, save, share

class EngagementRead(EngagementBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
