import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from app.bot.handlers import router
from app.config import settings

# инициализируем подключение к боту
bot = Bot(token=settings.TG_TOKEN)
# основной роутер - обрабатывает входящие обновления
dp = Dispatcher()

# поллинг - бесконечный цикл
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')