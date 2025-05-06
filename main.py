import asyncio
from aiogram import Bot, Dispatcher

from handlers import user_commands

from data.database import initialize_db
from config import TOKEN


async def main():
    await initialize_db()

    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
