from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///culinary_book.db"

async_engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(
    engine=async_engine,
    class_=AsyncSession,
)
