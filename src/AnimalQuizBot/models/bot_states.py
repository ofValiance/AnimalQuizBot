from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    in_menu = State()
    taking_quiz = State()
    leaving_review = State()
    waiting_for_comment = State()