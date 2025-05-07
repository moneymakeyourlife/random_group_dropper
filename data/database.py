import random
from datetime import datetime, timedelta
import aiosqlite
from config import DB_PATH


async def initialize_db():
    """
    Инициализирует базу данных, если она еще не существует.
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY
                )
            """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id INTEGER,
                    name TEXT
                )
            """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS links_counter (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    channel_id INTEGER,
                    date TEXT
                )
            """
            )
            await db.commit()
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")


async def add_user_if_not_exists(user_id: int) -> bool:
    """
    Добавляет user_id в таблицу users, если его там нет.
    Возвращает True, если добавление прошло успешно, иначе False.

    :param user_id: Идентификатор пользователя, который нужно добавить.
    :return: True, если user_id был добавлен, False, если он уже существует.
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                result = await cursor.fetchone()

            if result is None:
                await db.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
                await db.commit()
                return True
            else:
                return False
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return False


async def add_channel(channel_id: int, name: str) -> bool:
    """
    Добавляет канал в таблицу channels, если его там нет.
    Возвращает True, если добавление прошло успешно, иначе False.

    :param channel_id: Идентификатор канала
    :param name: Название канала
    :return: True, если был добавлен, False, если он уже существует.
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT 1 FROM channels WHERE channel_id = ?", (channel_id,)
            ) as cursor:
                result = await cursor.fetchone()

            if result is None:
                await db.execute(
                    "INSERT INTO channels (channel_id, name) VALUES (?,?)",
                    (
                        channel_id,
                        name,
                    ),
                )
                await db.commit()
                return True
            else:
                return False
    except Exception as e:
        print(f"Ошибка при добавлении канала: {e}")
        return False


async def delete_channel(channel_id: int) -> bool:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("DELETE FROM channels WHERE id = ?", (int(channel_id),))
            await db.commit()
    except Exception as e:
        print(f"Ошибка при добавлении канала: {e}")
        return False


async def get_all_channels():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM channels") as cur:
            result = await cur.fetchall()
            return result


async def get_channel_info(id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM channels WHERE id = ?", (id,)) as cursor:
            result = await cursor.fetchone()
            return result


async def get_random_channel_for_user(user_id: int):
    today = datetime.now().strftime("%d.%m.%Y")
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT COUNT(*) FROM links_counter WHERE user_id = ?", (user_id,)
            ) as cursor:
                total_links = (await cursor.fetchone())[0]

            if total_links >= 2:
                return None

            async with db.execute("SELECT channel_id FROM channels") as cursor:
                all_channels = [row[0] for row in await cursor.fetchall()]

            if not all_channels:
                return None

            async with db.execute(
                "SELECT channel_id FROM links_counter WHERE user_id = ?", (user_id,)
            ) as cursor:
                used_channels = [row[0] for row in await cursor.fetchall()]

            available_channels = [ch for ch in all_channels if ch not in used_channels]

            if not available_channels:
                return None

            selected_channel = random.choice(available_channels)

            await db.execute(
                "INSERT INTO links_counter (user_id, channel_id, date) VALUES (?, ?, ?)",
                (user_id, selected_channel, today),
            )
            await db.commit()

            return selected_channel
    except Exception as e:
        print(f"ошибка при получении канала: {e}")
        return None


async def get_total_stats_text():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(DISTINCT user_id) FROM links_counter"
        ) as cursor:
            active_users = (await cursor.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM links_counter") as cursor:
            total_links = (await cursor.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            total_users = (await cursor.fetchone())[0]

        return (
            f"📊 <b>общая статистика:</b>\n"
            f"👥 всего пользователей в боте: <b>{total_users}</b>\n"
            f"🔗 всего выдано ссылок: <b>{total_links}</b>\n"
            f"🧑‍💻 получили хотя бы одну ссылку: <b>{active_users}</b>"
        )


async def get_30_days_stats_text():
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%d.%m.%Y")
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(DISTINCT user_id) FROM links_counter WHERE date >= ?",
            (thirty_days_ago,),
        ) as cursor:
            active_users = (await cursor.fetchone())[0]

        async with db.execute(
            "SELECT COUNT(*) FROM links_counter WHERE date >= ?", (thirty_days_ago,)
        ) as cursor:
            total_links = (await cursor.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            total_users = (await cursor.fetchone())[0]

        return (
            f"📊 <b>статистика за 30 дней:</b>\n"
            f"👥 всего пользователей в боте: <b>{total_users}</b>\n"
            f"🔗 выдано ссылок за 30 дней: <b>{total_links}</b>\n"
            f"🧑‍💻 получили хотя бы одну ссылку: <b>{active_users}</b>"
        )
