import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogram import F

import transc_db
from qustion_processing import get_question
from output_answer import user_answer



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '7187855773:AAHS4TaoAcqAVgTOgjQqdqs196EN7w5Hgfo'


# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

            
async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза и баллы аользователя в 0
    current_question_index = 0
    user_count = 0
    await transc_db.update_quiz(user_id, current_question_index, user_count)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"), types.KeyboardButton(text="Показать последний результат"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Хэндлер на команды /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!", reply_markup=types.ReplyKeyboardRemove())
    # Запускаем новый квиз
    await new_quiz(message)

@dp.message(F.text=="Показать последний результат")
async def save_results(message: types.Message):
    user_id = message.from_user.id
    user_count = await transc_db.get_user_count(user_id)
    await message.answer(f"Ваш послений результат: {user_count}")


@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await user_answer(callback=callback, wr_or_rt="right_answer")

@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await user_answer(callback=callback, wr_or_rt='wrong_answer')


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(transc_db.create_table())
    asyncio.run(main())