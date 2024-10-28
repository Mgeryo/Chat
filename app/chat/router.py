import asyncio
from fastapi import APIRouter, Request, Response, WebSocket, WebSocketDisconnect, Depends, Header
from app.chat.models import Messages
from app.database import async_session_maker, get_async_session
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache


from app.tasks.tasks import send_messages
from app.users.auth import create_access_token
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)
# класс, который хранит в себе активные вебсокеты, чтобы можно было с ними общаться
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    # подключение нового пользователя
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    # удаление вебсокета из списка
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    # отправка персонального сообщения только одному клиенту
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        
    # для отправки всем клиентам
    async def broadcast(self, message: str, add_to_db: bool):
        # сперва вызываем функцию по отправке сообщения в бд
        # проверяем флаг - отправка разрешена
        if add_to_db: 
            await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    # функция сохраняющая в базу данных отправленные сообщения
    async def add_messages_to_database(message: str):
        # открываем контекстный менеджер
        async with async_session_maker() as session:
            stmt = insert(Messages).values(
                message=message
                )
            # выполняем и коммитим строчку, для отправки в бд
            await session.execute(stmt)
            await session.commit()
            
            
manager = ConnectionManager()

# эндпоинт для получения истории сообщений
@router.get("/last_messages")
@cache(expire=60)
async def get_last_messages(
    session: AsyncSession = Depends(get_async_session)
):
    query = select(Messages).order_by(Messages.id.desc())
    messages = await session.execute(query)
    messages = messages.all()
    # конвертируем словарик в JSON
    messages_list = [msg[0].as_dict() for msg in messages]
    # возвращаем в JSON формате
    return messages_list



# получаем fetch запрос с js(с куками), обработав куки в Depends получаем пользователя и возвращаем его имя
@router.get("/user")
def send_username(user: Users = Depends(get_current_user)):
    data = user.username
    return Response(content=data, media_type="text/plain")


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id):
    await manager.connect(websocket)
    try:
        while True:
            # ждем сообщение от клиента
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db = True) 
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db = False) # add_to_db разрешаем или не разрешаем запись в бд