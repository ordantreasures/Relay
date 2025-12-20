from pydantic import BaseModel
from datetime import datetime

class ReportBase(BaseModel):
    reason: str

class ReportCreate(ReportBase):
    post_id: int
    user_id: int

class ReportRead(ReportBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
