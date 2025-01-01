from aiogram import  types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import  ReplyKeyboardBuilder
from keyboards.inline import main_menu_keyboard


def register_handlers(dp):
    dp.message.register(cmd_start, Command("start"))
    
async def cmd_start(message: types.Message):
    keyboard = main_menu_keyboard()  
    await message.answer("Добро пожаловать в квиз! Выберите действие:", reply_markup=keyboard)
