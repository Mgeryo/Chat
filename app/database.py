from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# генерируем url
DATABASE_URL = settings.DATABASE_URL
DATABASE_PARAMS = {}

# создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
# создаем генератор сессий (транзакций)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# все модели алхимии будут наследоваться от этого класса
class Base(DeclarativeBase):
    pass