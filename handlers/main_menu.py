from aiogram import types
from aiogram import F
from keyboards.inline import main_menu_keyboard, choose_difficulty
from database.db_utils import get_user_stats, get_user_difficulty


def register_handlers(dp):
    dp.callback_query.register(handle_main_menu, F.data.in_({"start_quiz", "show_stats", "exit"}))

async def handle_main_menu(callback: types.CallbackQuery):
    actions = {
        "start_quiz": lambda: choose_difficulty(callback.message),
        "show_stats": lambda: show_user_stats(callback)
    }
    await actions[callback.data]()

async def show_user_stats(callback: types.CallbackQuery):
    correct, total, date = await get_user_stats(callback.from_user.id)  
    difficulty_map = {
        "easy": "Легкий",
        "medium": "Средний",
        "hard": "Сложный",
    }
    difficulty = await get_user_difficulty(callback.from_user.id)
    difficulty = difficulty_map.get(difficulty)
    result_message = f"Ваши результаты: {correct} правильных ответов из {total}.\nУровень теста: {difficulty}\nВремя последного прохождения: {date}" if total else "Вы еще не проходили квиз."
    await callback.message.answer(result_message,  reply_markup=main_menu_keyboard())
