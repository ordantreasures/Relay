from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(50))  # e.g., new_comment, post_trending
    message = Column(String(255))
    is_read = Column(Integer, default=0)  # 0 = unread, 1 = read
    created_at = Column(DateTime(timezone=True), server_default=func.now())
