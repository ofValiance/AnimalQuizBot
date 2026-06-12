from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.fsm.context import FSMContext

from src.AnimalQuizBot.models.bot_states import BotStates
from src.AnimalQuizBot.utils.keyboards import create_inline_keyboard


router = Router()

async def send_menu(message: Message, state: FSMContext):
    await state.set_state(BotStates.in_menu)
    buttons = [
        [("Пройти еще раз", "retry")],
        [("Оставить отзыв", "review"), ("Связаться", "contact")]
    ]
    keyboard = create_inline_keyboard(buttons)

    await message.answer(text="Меню:", reply_markup=keyboard)

async def delete_menu(query: Message | CallbackQuery, state: FSMContext):
    if await state.get_state() == BotStates.in_menu:
        if isinstance(query, Message):
            await query.delete()
        else:
            await query.message.delete()
    else:
        return