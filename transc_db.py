import aiosqlite

async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, user_count INTEGER)''')
        # Сохраняем изменения
        await db.commit()

# Запускаем создание таблицы базы данных

async def update_quiz(user_id, index, user_count):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, user_count) VALUES (?, ?, ?)', (user_id, index, user_count))
        # Сохраняем изменения
        await db.commit()



async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect('quiz_bot.db') as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results[0] is not None:
                return results[0]
            else:
                return 0
            
async def get_user_count(user_id):
    async with aiosqlite.connect('quiz_bot.db') as db:
        async with db.execute('SELECT user_count FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            count = await cursor.fetchone()
            if count[0] != 0:
                return count[0]
            else:
                return 0