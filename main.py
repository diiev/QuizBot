import asyncio
from config import dp, bot
from database.db_utils import create_table
from handlers import register_handlers

register_handlers(dp)

# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем создание таблицы базы данных
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())