from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# создаем клавиатуру
main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Запросить историю сообщений', callback_data = 'history')],
],                      
    resize_keyboard=True)