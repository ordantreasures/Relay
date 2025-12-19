from fastapi import FastAPI
from app.api.v1 import feed, posts, comments, categories, trending, auth, users

app = FastAPI(title="Relay Backend API")

app.include_router(feed.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(comments.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(trending.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
