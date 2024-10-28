from app.chat.models import Messages
from app.dao.base import BaseDAO

# передаем модель в класс и работаем с этой моделью
class MessagesDAO(BaseDAO):
    model = Messages