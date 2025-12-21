import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:ordan123@localhost:5432/relay"
engine = create_async_engine(DATABASE_URL)

async def test():
    async with engine.begin() as conn:
        from sqlalchemy import text
        result = await conn.execute(text("SELECT 1"))
        print(result.fetchall())

asyncio.run(test())
