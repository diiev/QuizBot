from aiogram import  types
from aiogram.filters.command import Command
from aiogram import F
from utils.quiz_loader import load_questions
from database.db_utils import update_quiz_index, get_quiz_index, get_user_difficulty
from keyboards.inline import generate_options_keyboard


QUESTIONS = load_questions("question.json")

def register_handlers(dp):
    dp.message.register(cmd_quiz, F.text=="Начать игру")
    dp.message.register(set_difficulty, F.text.in_({"Легкий", "Средний", "Сложный"}))
    dp.callback_query.register(right_answer, F.data=="right_answer")
    dp.callback_query.register(wrong_answer,F.data=="wrong_answer")
   


async def set_difficulty(message: types.Message):
    await message.answer(f"Вы выбрали уровень: {message.text}. Давайте начнем квиз!")
    await new_quiz(message)



async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await set_difficulty(message)


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0 
    difficulty_map = {"Легкий": "easy", "Средний": "medium", "Сложный": "hard"}
    difficulty = difficulty_map[message.text]
    await update_quiz_index(user_id, current_question_index, difficulty)
    await get_question(message, user_id)



async def get_question(message, user_id): 
    filtered_questions = await get_filtered_questions(user_id)
    if not filtered_questions:
        await message.answer("Нет доступных вопросов для выбранного уровня сложности.")
        return
    QUESTIONS = filtered_questions 
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    question_data = QUESTIONS[current_question_index]
    correct_index = question_data['correct_option']
    opts = question_data['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{question_data['question']}", reply_markup=kb)


async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    await callback.message.answer("Верно!")
    current_question_index = await get_quiz_index(callback.from_user.id)
    difficulty = await get_user_difficulty(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index, difficulty)


    if current_question_index < len(QUESTIONS):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = QUESTIONS[current_question_index]['correct_option'] 
    difficulty = await get_user_difficulty(callback.from_user.id)

    await callback.message.answer(f"Неправильно {}. Правильный ответ: {QUESTIONS[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index, difficulty)


    if current_question_index < len(QUESTIONS):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


async def get_filtered_questions(user_id):
    difficulty = await get_user_difficulty(user_id)
    filtered = [q for q in QUESTIONS if q["difficulty"] == difficulty]
    return filtered
