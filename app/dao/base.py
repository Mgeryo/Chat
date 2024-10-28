from app.database import async_session_maker
from sqlalchemy import insert, select

# Основной класс работы с БД
class BaseDAO:
    model = None
    
    # метод для добавления данных в бд
    @classmethod 
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query) 
            await session.commit()  
    
    # метод - либо найди либо верни None        
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        
    # метод - найди все
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()