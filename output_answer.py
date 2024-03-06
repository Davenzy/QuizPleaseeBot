from aiogram import Dispatcher
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

import transc_db
from qustion_processing import get_question
from quiz_data import quiz_data

dp = Dispatcher()

async def user_answer(callback, wr_or_rt):
    # Получение текущего вопроса для данного пользователя
    current_question_index = await transc_db.get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    count = await transc_db.get_user_count(callback.from_user.id)

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    if wr_or_rt == 'right_answer':
        # Отправляем в чат сообщение, что ответ верный
        await callback.message.answer("Верно!")
        count += 1


    elif wr_or_rt == 'wrong_answer':
        # Отправляем в чат сообщение об ошибке с указанием верного ответа
        await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных и счетчик баллов
    current_question_index += 1
    await transc_db.update_quiz(callback.from_user.id, current_question_index, count)
    
    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        count = await transc_db.get_user_count(callback.from_user.id)
        
        builder = ReplyKeyboardBuilder()
        # Добавляем в сборщик одну кнопку
        builder.add(types.KeyboardButton(text="Начать игру"), types.KeyboardButton(text="Показать последний результат"))

        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer("Подсчитываем баллы ...")
        await callback.message.answer(f"Ваш результат: {count}", reply_markup=builder.as_markup(resize_keyboard=True))


