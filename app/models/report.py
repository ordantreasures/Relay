from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
