from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import settings

# Synchronous database setup
print(f"DEBUG: Using database URL: {settings.database_url}")
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous database setup
# Handle both PostgreSQL and SQLite URLs
if settings.database_url.startswith("postgresql://"):
    async_database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
else:
    # For SQLite, use aiosqlite
    async_database_url = settings.database_url.replace("sqlite://", "sqlite+aiosqlite://")

async_engine = create_async_engine(
    async_database_url,
    echo=settings.debug
)
AsyncSessionLocal = async_sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as session:
        yield session

