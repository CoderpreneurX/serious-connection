from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core.config import settings

# Base class for models
Base = declarative_base()

# Async database engine
# Note: For Postgres: "postgresql+asyncpg://user:pass@host/db"
# For SQLite: "sqlite+aiosqlite:///./dev.db"
engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    echo=settings.DEBUG,  # log SQL in dev
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Dependency for FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
