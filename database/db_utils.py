import aiosqlite
from config import DB_NAME



async def update_user_difficulty(user_id, difficulty):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_state (user_id, question_index, difficulty)
            VALUES (?, COALESCE((SELECT question_index FROM quiz_state WHERE user_id = ?), 0), ?)
        ''', (user_id, user_id, difficulty))
        await db.commit()
        print(f"update_user_difficulty: user_id={user_id}, difficulty={difficulty}") 
        



async def get_user_difficulty(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT difficulty FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone() 
            print(f"get_user_difficulty: user_id={user_id}, result={result}")
            cursor.execute("PRAGMA table_info(quiz_state);")
            return result[0] if result else "easy" 
       

async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()


async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute('''
                         CREATE TABLE IF NOT EXISTS quiz_state (
                         user_id INTEGER PRIMARY KEY, 
                         question_index INTEGER,
                         difficulty TEXT
                         )
                         ''')
        # Сохраняем изменения
        await db.commit()
