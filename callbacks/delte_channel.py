from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from data.database import delete_channel, get_channel_info
from config import ADMIN_ID

router = Router()


@router.callback_query(F.data.startswith("del_channel_"))
async def start_del_channel(call: CallbackQuery, bot: Bot):
    channel_id = call.data.split("del_channel_")[-1]
    channel_info = await get_channel_info(channel_id)

    kb = [
        [
            InlineKeyboardButton(
                text="✅ Да, удалить", callback_data=f"accept_del_{channel_id}"
            )
        ],
        [InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await bot.send_message(
        chat_id=call.from_user.id,
        text=f"⁉️ Вы действительно хотите удалить {channel_info[2]}?",
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("accept_del_"))
async def end_del_channel(call: CallbackQuery, bot: Bot):
    channel_id = call.data.split("accept_del_")[-1]
    channel_info = await get_channel_info(channel_id)
    await delete_channel(channel_id)

    await bot.send_message(
        chat_id=call.from_user.id,
        text=f"🥳 Вы успешно удалили канал {channel_info[2]}?",
    )
