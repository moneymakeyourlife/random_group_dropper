from aiogram import Router, Bot

from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from data.database import add_channel

from config import ADMIN_ID

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bot_added(event: ChatMemberUpdated, bot: Bot):
    try:
        chat = await bot.get_chat(event.chat.id)
        admins = await bot.get_chat_administrators(event.chat.id)

        if chat.username:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Вы хотели добавить бота в канал: {chat.title}\nКАНАЛ ДОЛЖЕН БЫТЬ ПРИВАТНЫМ!",
            )
            await bot.leave_chat(chat.id)
            return

        admin_list = []
        admin_int_list = []
        for admin in admins:
            if admin.user.is_bot:
                continue

            user_id = admin.user.id
            admin_list.append(f"<code>{user_id}</code>")
            admin_int_list.append(user_id)

        if ADMIN_ID not in admin_int_list:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🚨 кто-то хотел добавить бота в канал <b>{chat.title}</b>(<code>{chat.id}</code>)\n\n",
                parse_mode="html",
            )

        is_added = await add_channel(channel_id=chat.id, name=chat.title)

        if is_added:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"🔥\nбот добавлен в <b>{chat.title}</b>\n\n"
                    f"id канала: <code>{chat.id}</code>\n\n"
                    f"администраторы: {admin_list}"
                ),
                parse_mode="html",
            )

        else:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"❌\nбот НЕ добавлен в <b>{chat.title}</b>\n\n"
                    f"id канала: <code>{chat.id}</code>\n\n"
                    f"администраторы: {admin_list}\nОШИБКА ПРИ ДОБАВЛЕНИИ КАНАЛА!"
                ),
                parse_mode="html",
            )
    except:
        pass
