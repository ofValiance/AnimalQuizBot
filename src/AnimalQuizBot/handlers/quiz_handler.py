from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import urllib.parse

from src.AnimalQuizBot.utils.keyboards import create_inline_keyboard, create_link_inline_keyboard
from src.AnimalQuizBot.services.scores_service import gather_scores, pick_animal
from src.AnimalQuizBot.models.bot_states import BotStates
from src.AnimalQuizBot.handlers.menu_handler import send_menu, delete_menu

from src.AnimalQuizBot.data import QUIZ_DATA, ANIMALS_DATA, IMAGES_PATH
from src.AnimalQuizBot import BOT_USERNAME


router = Router()

@router.callback_query(F.data == "retry", BotStates.in_menu)
async def start_quiz(query: Message | CallbackQuery, state: FSMContext):
    await state.update_data(
        cur_question_index = 0,
        answers = {},
        animal = None
    )
    await delete_menu(query, state)
    await state.set_state(BotStates.taking_quiz)

    if isinstance(query, Message):
        await query.answer("Поехали!")
    else:
        await query.message.answer("Поехали!")
    await send_question(query, state)

async def send_question(query: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    q_index = data["cur_question_index"]

    if q_index >= len(QUIZ_DATA.questions):
        await finish_quiz(query)
        return

    question = QUIZ_DATA.questions[q_index]
    question_text = (
            f"{question.text}\n\n" +
            "\n".join(f"{option.id}. {option.emoji} {option.text}" for option in question.options)
    )

    buttons = []
    for option in question.options:
        b_text = f"{option.id}. {option.emoji}"
        b_callback = f"answer_{question.id}_{option.id}"
        button = (b_text, b_callback)
        buttons.append(button)
    keyboard = create_inline_keyboard([buttons])

    if isinstance(query, Message):
        await query.answer(question_text, reply_markup=keyboard)
    else:
        await query.answer()
        await query.message.answer(question_text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("answer_"), BotStates.taking_quiz)
async def process_answer(callback: CallbackQuery,  state: FSMContext):
    _, q_id, option_id = callback.data.split("_")
    q_id = int(q_id)
    option_id = int(option_id)

    data = await state.get_data()
    q_index = data["cur_question_index"]
    question = QUIZ_DATA.questions[q_index]

    answers = data["answers"]
    answers[q_id] = option_id
    await state.update_data(
        cur_question_index = q_index + 1,
        answers = answers
    )

    await callback.answer()
    await callback.message.edit_text(question.text, reply_markup=None)

    answer_text = f"{question.options[option_id - 1].emoji} {question.options[option_id - 1].text}"

    await callback.message.answer(answer_text)
    await send_question(callback, state)

async def finish_quiz(query: Message | CallbackQuery):
    finish_text = "Тест пройден!"
    buttons = [
        [("Узнать результат!", "result")]
    ]
    keyboard = create_inline_keyboard(buttons)
    if isinstance(query, Message):
        await query.answer(finish_text, reply_markup=keyboard)
    else:
        await query.message.answer(finish_text, reply_markup=keyboard)

@router.callback_query(F.data == "result", BotStates.taking_quiz)
async def show_result(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    answers = data["answers"]
    scores = await gather_scores(answers)
    animal = ANIMALS_DATA.root.get(await pick_animal(scores))
    await state.update_data(
        animal = animal
    )

    image = FSInputFile(path=IMAGES_PATH / animal.image)
    result_text = (
        f"🎉 Поздравляем! Твое тотемное животное в Московском зоопарке — {animal.emoji} {animal.name}!\n\n"
        f"{animal.description}\n\n"
        f"{animal.custody}\n\n"
        f"🤝 Стань опекуном! Да, в Московском зоопарке вы можете финансово помочь вашему тотемному животному и обеспечить лучшие условия для жизни, поучаствовав в <a href='https://moscowzoo.ru/about/guardianship'>программе опеки</a>.\n\n"
        f"Поделиться:"
    )

    bot_link = f"https://t.me/{BOT_USERNAME}"

    share_title = f"Викторина Московского зоопарка"

    share_text = (
        f"Я прошел викторину Московского зоопарка!\n"
        f"Мое тотемное животное: {animal.name}! Я узнал, что могу помочь ему с помощью программы опеки.\n"
        f"Ты тоже можешь найти свое животное и сделать его жизнь лучше: {bot_link}"
    )

    encoded_bot_link = urllib.parse.quote(bot_link)
    encoded_share_title = urllib.parse.quote(share_title)
    encoded_share_text = urllib.parse.quote(share_text)

    share_buttons = [
        [
            ("Telegram", f"https://t.me/share/url?url={encoded_bot_link}&text={encoded_share_text}"),
            ("VK", f"https://vk.com/share.php?url={encoded_bot_link}&title={encoded_share_title}&description={encoded_share_text}"),
            ("WhatsApp", f"https://wa.me/?text={encoded_share_text}")
        ]
    ]

    keyboard = create_link_inline_keyboard(share_buttons)

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.bot.send_photo(chat_id=callback.message.chat.id, photo=image, caption=result_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    await send_menu(callback.message, state)