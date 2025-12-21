from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.cors import setup_cors
from app.core.exeception_handlers import setup_exception_handlers
from app.core.logging_config import setup_logging, RequestLogger, request_logging_middleware
from app.api.v1 import feed, health, posts, comments, categories, trending, auth, users, moderation

# Setup logging
setup_logging()

# Create app
app = FastAPI(
    title="Relay API",
    description="Social content sharing platform",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)


@app.get("/")
def read_root():
    return {"message": "FastAPI on Railway", "status": "running"}


# Add middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=request_logging_middleware)

# Force HTTPS in production
if not settings.DEBUG:
    app.add_middleware(HTTPSRedirectMiddleware)

# Setup CORS
setup_cors(app)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(feed.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(comments.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(trending.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(moderation.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
