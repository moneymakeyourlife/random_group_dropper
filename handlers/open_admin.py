from aiogram import Router, F
from aiogram.types import Message

from keyboards.admin_inline import get_admin_menu
from config import ADMIN_ID

router = Router()


@router.message(F.text == "/admin")
async def admin_start_func(msg: Message):
    user_id = msg.from_user.id

    if user_id == ADMIN_ID:
        await msg.answer(
            text=f"ADMINKA, <b>{msg.from_user.full_name}</b>",
            parse_mode="html",
            reply_markup=await get_admin_menu(),
        )
