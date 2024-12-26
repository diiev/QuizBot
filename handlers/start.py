from aiogram import  types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import  ReplyKeyboardBuilder
from keyboards.reply import choose_difficulty


def register_handlers(dp):
    dp.message.register(cmd_start, Command("start"))
    
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))
    await choose_difficulty(message)
