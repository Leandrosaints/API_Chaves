from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from API.core.config import settings

engine:AsyncEngine = create_async_engine(settings.DB_URL)

Session:AsyncSession = sessionmaker(

    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)