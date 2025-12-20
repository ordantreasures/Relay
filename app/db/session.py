from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postman@localhost:5432/relay"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

from sqlalchemy.ext.asyncio import async_sessionmaker

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
