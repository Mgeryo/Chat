from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
import app.bot.keyboards as kb
import app.bot.requests as rq

router = Router()

# декоратор, работает с коммандой start
@router.message(CommandStart())
# принимаем объект класса Message
async def cmd_start(message: Message):
    # метод answer у этого класса позволяет отвечать этому же пользователю
    await message.reply(f'Привет.\nТвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}',
                        reply_markup=kb.main
                        )


# перехватываем коллбек и работаем с ним    
@router.callback_query(F.data == 'history')
async def history(callback: CallbackQuery):
    data = await rq.get_history()
    for i in data:
        await callback.message.answer(i['message'])