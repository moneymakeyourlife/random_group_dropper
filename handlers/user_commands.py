from aiogram import Router, F
from aiogram.types import Message

from keyboards.user_inline import get_main_menu
from data.database import add_user_if_not_exists

router = Router()


@router.message(F.text == "/start")
async def start_func(msg: Message):
    user_id = msg.from_user.id
    await add_user_if_not_exists(user_id)

    await msg.answer(
        text=f"👋 Привет, <b>{msg.from_user.full_name}</b>",
        parse_mode="html",
        reply_markup=await get_main_menu(),
    )
