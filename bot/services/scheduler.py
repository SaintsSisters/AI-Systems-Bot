import logging
import random
import datetime
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from telegram.error import TelegramError

from bot.data.daily_drops import DAILY_DROPS
from bot.services.subscribers import get_active_subscribers, already_sent_today, mark_sent
from bot.utils.lang import get_lang

logger = logging.getLogger(__name__)

DAILY_DROP_HOUR = 18
DAILY_DROP_MINUTE = 0


def _pick_drop_for_today() -> dict:
    today = datetime.date.today()
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    return random.choice(DAILY_DROPS)


def _format_drop(drop: dict, lang: str) -> str:
    system = drop["system_ru"] if lang == "ru" else drop["system_en"]
    prompt = drop["prompt_ru"] if lang == "ru" else drop["prompt_en"]
    action = drop["action_ru"] if lang == "ru" else drop["action_en"]
    divider = "─" * 26
    footer = (
        "_Возвращайся завтра за следующим дропом._"
        if lang == "ru"
        else "_Come back tomorrow for the next drop._"
    )
    s_label = "Система" if lang == "ru" else "System"
    p_label = "Промпт" if lang == "ru" else "Prompt"
    a_label = "Действие" if lang == "ru" else "Action"
    return (
        f"⚡ *DAILY DROP*\n"
        f"{divider}\n\n"
        f"🔧 *{s_label}:* {system}\n\n"
        f"📋 *{p_label}:*\n{prompt}\n\n"
        f"🎯 *{a_label}:*\n{action}\n\n"
        f"{divider}\n{footer}"
    )


async def send_daily_drops_job(context: CallbackContext) -> None:
    subscribers = get_active_subscribers()
    if not subscribers:
        logger.info("Daily drop: no active subscribers, skipping.")
        return

    drop = _pick_drop_for_today()
    sent = 0
    skipped = 0

    for user_id in subscribers:
        if already_sent_today(user_id):
            skipped += 1
            continue
        try:
            lang = get_lang(user_id)
            message = _format_drop(drop, lang)
            await context.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
            )
            mark_sent(user_id)
            sent += 1
        except TelegramError as e:
            logger.warning(f"Daily drop failed for user {user_id}: {e}")

    logger.info(f"Daily drop: {sent} delivered, {skipped} already sent today.")


def register_daily_drop_job(app) -> None:
    drop_time = datetime.time(
        hour=DAILY_DROP_HOUR,
        minute=DAILY_DROP_MINUTE,
        tzinfo=datetime.timezone.utc,
    )
    app.job_queue.run_daily(
        send_daily_drops_job,
        time=drop_time,
        name="daily_drop",
    )
    logger.info(f"Daily Drop job registered — fires at {DAILY_DROP_HOUR:02d}:{DAILY_DROP_MINUTE:02d} UTC.")
