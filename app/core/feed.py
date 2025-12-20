import json
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from app.models.engagement import Engagement
from app.schemas.post import PostRead
from app.core.cache import get_cached, set_cache


async def get_feed_posts(db: AsyncSession, limit: int = 20, offset: int = 0, use_cache: bool = True):
    """
    Returns posts ranked by a combination of:
    - Engagement score (likes, shares, comments)
    - Recency (newer posts favored)
    Uses Redis caching for performance.
    """
    cache_key = f"feed:{limit}:{offset}"

    # Check cache first
    if use_cache:
        cached = await get_cached(cache_key)
        if cached:
            return [PostRead.parse_raw(p) for p in json.loads(cached)]

    # --- DB Query ---
    engagement_subq = (
        select(
            Engagement.post_id,
            func.count(Engagement.id).label("engagement_count")
        ).group_by(Engagement.post_id).subquery()
    )

    stmt = (
        select(Post, func.coalesce(engagement_subq.c.engagement_count, 0).label("score"))
        .outerjoin(engagement_subq, Post.id == engagement_subq.c.post_id)
        .order_by(func.coalesce(engagement_subq.c.engagement_count, 0).desc(), Post.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(stmt)
    posts = [p[0] for p in result.fetchall()]

    # Cache the result
    if use_cache:
        posts_json = [PostRead.from_orm(p).json() for p in posts]
        await set_cache(cache_key, json.dumps(posts_json), expire=300)

    return posts
