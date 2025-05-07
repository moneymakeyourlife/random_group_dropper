from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_admin_menu():
    kb = [
        [InlineKeyboardButton(text="📊 Статистика", callback_data="all_statistic")],
        [
            InlineKeyboardButton(
                text="📊 Статистика за месяц", callback_data="month_statistic"
            )
        ],
        [InlineKeyboardButton(text="🔗 Каналы", callback_data="my_channels")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard
