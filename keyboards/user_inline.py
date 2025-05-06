from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_main_menu():
    kb = [[InlineKeyboardButton(text="🔗 Получить ссылку", callback_data="get_link")]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard
