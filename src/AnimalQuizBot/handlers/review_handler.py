from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from src.AnimalQuizBot.models.reviews import Review
from src.AnimalQuizBot.utils.keyboards import create_inline_keyboard
from src.AnimalQuizBot.models.bot_states import BotStates
from src.AnimalQuizBot.handlers.menu_handler import send_menu, delete_menu
from src.AnimalQuizBot.data import dl


router = Router()

@router.callback_query(F.data == "review", BotStates.in_menu)
async def leave_review(callback: CallbackQuery, state: FSMContext):
    await delete_menu(callback, state)
    await state.set_state(BotStates.leaving_review)
    await state.update_data(
        rating=None,
        comment=None
    )
    await pick_rating(callback.message, state)

async def pick_rating(message: Message, state: FSMContext):
    buttons = [
        [("1 ⭐", "rating_1"), ("2 ⭐", "rating_2"), ("3 ⭐", "rating_3"), ("4 ⭐", "rating_4"), ("5 ⭐", "rating_5")]
    ]
    keyboard = create_inline_keyboard(buttons)

    await message.answer("Оцени бота по пятибалльной шкале:", reply_markup = keyboard)

@router.callback_query(F.data.startswith("rating"), BotStates.leaving_review)
async def process_rating(callback: CallbackQuery, state: FSMContext):
    _, rating = callback.data.split("_")
    rating = int(rating)

    await state.update_data(
        rating = rating
    )

    await callback.message.edit_reply_markup(reply_markup = None)
    await callback.message.answer(f"{rating}")

    await callback.message.answer("Если хочешь, оставь комментарий:")
    await state.set_state(BotStates.waiting_for_comment)
    await callback.answer()

@router.message(BotStates.waiting_for_comment)
async def write_comment(message: Message, state: FSMContext):
    comment = message.text.strip()
    await state.update_data(
        comment = comment,
    )
    await state.set_state(BotStates.leaving_review)
    await process_review(message, state)

async def process_review(message: Message, state: FSMContext):
    data = await state.get_data()
    review = Review(
        user_id = message.chat.id,
        username = f"@{message.from_user.username}",
        animal = data["animal"].name,
        rating = data["rating"],
        comment = data["comment"]
    )
    await dl.download_review(review, "reviews.json")
    await message.answer("Спасибо! Твой отзыв сохранен!")

    await send_menu(message, state)
