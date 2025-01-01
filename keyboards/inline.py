from aiogram import  types
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for index, option in enumerate(answer_options):
        callback_data = f"answer_{index}_{'right' if option == right_answer else 'wrong'}"
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=callback_data)
        )

    builder.adjust(1)
    return builder.as_markup()



def main_menu_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Начать игру", callback_data="start_quiz")],
        [InlineKeyboardButton(text="📊 Моя статистика", callback_data="show_stats")]
    ])
    return kb



async def choose_difficulty(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🥉 Легкий", callback_data="easy")],
        [InlineKeyboardButton(text="🥈 Средний", callback_data="medium")],
        [InlineKeyboardButton(text="🥇 Сложный", callback_data="hard")]
    ])

    await message.answer("Выберите уровень сложности:", reply_markup=keyboard)
