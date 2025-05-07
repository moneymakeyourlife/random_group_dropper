from aiogram import Router, F, Bot
from aiogram.types import Message

from data.database import add_user_if_not_exists, get_random_channel_for_user

router = Router()


@router.message(F.text == "/start")
async def start_func(msg: Message, bot: Bot):
    user_id = msg.from_user.id
    await add_user_if_not_exists(user_id)
    channel_id = await get_random_channel_for_user(user_id)

    if channel_id is None:
        await msg.answer("<b>Превышено количество ссылок на Ваш аккаунт</b>")
        return

    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=channel_id, member_limit=1
        )
        await msg.answer(
            text=f"<b>Одноразовая ссылка:</b> {invite_link.invite_link}",
            parse_mode="HTML",
        )
    except Exception as e:
        await msg.answer(f"ошибка при генерации ссылки: {e}")
