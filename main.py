import asyncio
from aiogram import Bot, Dispatcher

from handlers import user_commands, add_channel, open_admin
from callbacks import my_channels, delte_channel, all_statistic

from data.database import initialize_db
from config import TOKEN


async def main():
    await initialize_db()

    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        add_channel.router,
        open_admin.router,
        my_channels.router,
        delte_channel.router,
        all_statistic.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
