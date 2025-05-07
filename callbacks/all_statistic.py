from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from data.database import get_30_days_stats_text, get_total_stats_text
from config import ADMIN_ID

router = Router()


@router.callback_query(F.data == "all_statistic")
async def print_all_stat(call: CallbackQuery, bot: Bot):

    stats = await get_total_stats_text()
    await bot.send_message(chat_id=ADMIN_ID, text=stats, parse_mode="HTML")


@router.callback_query(F.data == "month_statistic")
async def print_all_stat(call: CallbackQuery, bot: Bot):

    stats = await get_30_days_stats_text()
    await bot.send_message(chat_id=ADMIN_ID, text=stats, parse_mode="HTML")
