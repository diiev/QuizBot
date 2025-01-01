from aiogram import types
from .quiz import start_quiz
from aiogram import F


def register_handlers(dp):
    dp.callback_query.register(handle_difficulty_selection, F.data.in_({"easy", "medium", "hard"}))

async def handle_difficulty_selection(callback: types.CallbackQuery):
    difficulty_map = {
        "easy": "Легкий",
        "medium": "Средний",
        "hard": "Сложный",
    }
    selected_difficulty = difficulty_map.get(callback.data)

    if selected_difficulty:
        await callback.message.answer(f"Вы выбрали уровень: {selected_difficulty}. Давайте начнём!")
        await callback.message.delete()
        await start_quiz(callback, callback.data)
    else:
        await callback.answer("Неверный выбор.")