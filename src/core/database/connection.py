from fastapi import HTTPException

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.core.utils.config import settings

if not settings.db.DATABASE_URL:
    raise HTTPException(status_code=500, detail=f"DATABASE_URL нет в настройках на сервере (в .env)")

engine = create_async_engine(settings.db.DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            print(f"Database error: {e}")
            raise HTTPException(status_code=500, detail=f"Ошибка при получении сессии базы данных: {str(e)}")
