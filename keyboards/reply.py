from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import  types
async def choose_difficulty(message: types.Message):
    # Создаём клавиатуру с уровнями сложности
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Легкий"))
    builder.add(types.KeyboardButton(text="Средний"))
    builder.add(types.KeyboardButton(text="Сложный"))
    await message.answer("Выберите уровень сложности:", reply_markup=builder.as_markup(resize_keyboard=True))
