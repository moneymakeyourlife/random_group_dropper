from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from data.database import get_all_channels
from config import ADMIN_ID

router = Router()


@router.callback_query(F.data == "my_channels")
async def print_channels(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id

    if user_id == ADMIN_ID:
        channels = await get_all_channels()

        kb = []

        for channel in channels:
            kb.append(
                [
                    InlineKeyboardButton(
                        text=channel[2], callback_data=f"del_channel_{channel[0]}"
                    )
                ]
            )
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

        await bot.send_message(
            chat_id=user_id,
            text="⁉️ Выберите канал который хотите удалить",
            reply_markup=keyboard,
        )
