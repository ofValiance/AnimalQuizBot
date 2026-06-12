from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_reply_keyboard(buttons: list[list[str]]) -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=button_text) for button_text in row]
        for row in buttons
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)

def create_inline_keyboard(buttons: list[list[tuple]]) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text=button_text, callback_data=callback_text) for button_text, callback_text in row]
        for row in buttons
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def create_link_inline_keyboard(buttons: list[list[tuple]]) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text=button_text, url=link_text) for button_text, link_text in row]
        for row in buttons
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)