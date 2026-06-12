from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.AnimalQuizBot.handlers.quiz_handler import start_quiz


router = Router()

@router.message(Command("start"))
async def start_test_handler(message: Message, state: FSMContext):
    await state.update_data(
        cur_question_index=0,
        answers={},
        animal=None,
        rating=None,
        comment=None
    )
    await message.answer(text="Это бот-викторина. Ответьте на вопросы и найдите ваше тотемное животное среди зверей Московского зоопарка!")
    await start_quiz(message, state)