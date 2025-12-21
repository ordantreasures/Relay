from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Index
from sqlalchemy.sql import func
from app.db.base import Base

class Engagement(Base):
    __tablename__ = "engagements"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(20))  # like, save, share
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    Index("idx_engagements_post_id", "post_id")

