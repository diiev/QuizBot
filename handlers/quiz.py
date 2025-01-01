from aiogram import types
from aiogram import F
from database.db_utils import (
    update_quiz_state,
    get_quiz_index,
    get_user_difficulty,
    save_quiz_result,
    reset_quiz_result
)
from keyboards.inline import generate_options_keyboard, main_menu_keyboard, choose_difficulty
from utils.quiz_loader import ALL_QUESTIONS




def register_handlers(dp):
    dp.callback_query.register(handle_answer, F.data.regexp(r"^answer_\d+_(right|wrong)$"))




async def start_quiz(callback: types.CallbackQuery, difficulty):
    await update_quiz_state(callback.from_user.id, 0, difficulty)
    await reset_quiz_result(callback.from_user.id)
    await get_question(callback)

async def handle_answer(callback: types.CallbackQuery):
    data_parts = callback.data.split("_")
    if len(data_parts) != 3 or not data_parts[1].isdigit():
        await callback.message.answer("Ошибка: некорректные данные. Попробуйте снова.")
        return
    selected_option_index = int(data_parts[1])  
    is_correct = data_parts[2] == "right"  
    question = await get_filtered_questions(callback.from_user.id)
    current_question_index = await get_quiz_index(callback.from_user.id)
    question_data = question[current_question_index]
    user_answer = question_data['options'][selected_option_index]
    correct_option_index = question_data['correct_option']
    correct_answer = question_data['options'][correct_option_index]

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    if is_correct:
        await callback.message.answer(f"✅ Вы ответили '{user_answer}' и это - правильный ответ!")
        await save_quiz_result(callback.from_user.id, is_correct, len(question))
        
    else:
        await callback.message.answer(f"❌ Вы ответили '{user_answer}' и это - неправильно.\n✅ Правильный ответ: {correct_answer}")

   
    await process_next_question(callback)

async def process_next_question(callback: types.CallbackQuery):
    current_question_index = await get_quiz_index(callback.from_user.id) + 1
    await update_quiz_state(callback.from_user.id, current_question_index)

    question = await get_filtered_questions(callback.from_user.id)
    if current_question_index < len(question):
        await get_question(callback)
    else:
        await callback.message.answer("🏁 Это был последний вопрос. Квиз завершен!")
        await show_user_stats(callback)

async def get_question(callback: types.CallbackQuery):
    current_question_index = await get_quiz_index(callback.from_user.id)
    question = await get_filtered_questions(callback.from_user.id)
    question_data = question[current_question_index]

    kb = generate_options_keyboard(
        question_data['options'],
        question_data['options'][question_data['correct_option']]
    )
    await callback.message.answer(question_data['question'], reply_markup=kb)

async def get_filtered_questions(user_id):
    difficulty = await get_user_difficulty(user_id)
    return [q for q in ALL_QUESTIONS if q["difficulty"] == difficulty]
