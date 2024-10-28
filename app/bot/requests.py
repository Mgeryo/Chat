from app.chat.models import Messages
from app.database import async_session_maker, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.chat.dao import MessagesDAO

async def get_history(
):
    async with async_session_maker() as session:
         
        messages = await MessagesDAO.find_all()
        # возвращаем в JSON формате
        return messages