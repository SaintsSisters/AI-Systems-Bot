import logging
import random
import datetime
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from telegram.error import TelegramError

from bot.data.scheduled_drops import SCHEDULED_DROPS
from bot.services.subscribers import get_active_subscribers, already_sent_today, mark_sent

logger = logging.getLogger(__name__)

DAILY_DROP_HOUR = 18
DAILY_DROP_MINUTE = 0


def _pick_drop_for_today() -> dict:
    today = datetime.date.today()
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    return random.choice(SCHEDULED_DROPS)


def _format_scheduled_drop(drop: dict) -> str:
    return (
        f"⚡ *DAILY DROP*\n"
        f"─────────────────────────\n\n"
        f"💡 *Insight*\n{drop['insight']}\n\n"
        f"🎯 *Action*\n{drop['action']}\n\n"
        f"_{drop['cta']}_\n\n"
        f"─────────────────────────\n"
        f"_Come back tomorrow for another drop._"
    )


async def send_daily_drops_job(context: CallbackContext) -> None:
    subscribers = get_active_subscribers()
    if not subscribers:
        logger.info("Daily drop: no active subscribers, skipping.")
        return

    drop = _pick_drop_for_today()
    message = _format_scheduled_drop(drop)
    sent = 0
    skipped = 0

    for user_id in subscribers:
        if already_sent_today(user_id):
            skipped += 1
            continue
        try:
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
    drop_time = datetime.time(hour=DAILY_DROP_HOUR, minute=DAILY_DROP_MINUTE, tzinfo=datetime.timezone.utc)
    app.job_queue.run_daily(
        send_daily_drops_job,
        time=drop_time,
        name="daily_drop",
    )
    logger.info(f"Daily Drop job registered — fires at {DAILY_DROP_HOUR:02d}:{DAILY_DROP_MINUTE:02d} UTC.")
