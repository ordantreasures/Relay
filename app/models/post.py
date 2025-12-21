from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base





class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def soft_delete(self):
        self.is_deleted = True

    author = relationship("User", backref="posts")
    category = relationship("Category", backref="posts")
    
    
    # app/models/post.py

__table_args__ = (
    Index("idx_posts_created_at", "created_at"),
    Index("idx_posts_category", "category_id"),
    Index("idx_posts_not_deleted", "is_deleted"),
)