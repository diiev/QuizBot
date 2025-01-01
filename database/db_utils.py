import aiosqlite
from config import DB_NAME

async def get_user_difficulty(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT difficulty FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else "easy"

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0



async def update_quiz_state(user_id, question_index=None, difficulty=None):
    async with aiosqlite.connect(DB_NAME) as db:
        # Обновляем состояние викторины, создавая запись, если её нет
        await db.execute('''
            INSERT INTO quiz_state (user_id, question_index, difficulty)
            VALUES (
                ?, 
                COALESCE(?, (SELECT question_index FROM quiz_state WHERE user_id = ?), 0),
                COALESCE(?, (SELECT difficulty FROM quiz_state WHERE user_id = ?), "easy")
            )
            ON CONFLICT(user_id) DO UPDATE SET 
                question_index = COALESCE(excluded.question_index, quiz_state.question_index),
                difficulty = COALESCE(excluded.difficulty, quiz_state.difficulty)
        ''', (user_id, question_index, user_id, difficulty, user_id))
        await db.commit()




# Новая функция: сохранение результата квиза
async def save_quiz_result(user_id, correct_answers, total_questions):
    async with aiosqlite.connect(DB_NAME) as db:
        if correct_answers == 1:
            await db.execute('''
                 INSERT INTO quiz_results (user_id, correct_answers, total_questions)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id) 
        DO UPDATE SET correct_answers = correct_answers + 1, total_questions = $3, date = CURRENT_TIMESTAMP;
            ''', (user_id, correct_answers, total_questions))
       
        await db.commit()

async def reset_quiz_result(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                '''
                  UPDATE quiz_results
        SET correct_answers = 0,
            total_questions = 0,
            date = CURRENT_TIMESTAMP
            WHERE user_id = ?;
            ''', (user_id,) 
            )
       
            await db.commit()



# Новая функция: получение статистики
async def get_user_stats(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers, total_questions, date FROM quiz_results WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result if result else (0, 0, 0)

# Создание таблиц
async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY, 
                question_index INTEGER,
                difficulty TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER PRIMARY KEY,
                correct_answers INTEGER,
                total_questions INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                         
            )
        ''')
        await db.commit()



