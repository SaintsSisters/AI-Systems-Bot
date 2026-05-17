import logging
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="telegram")

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from bot.handlers.menu import start, handle_callback
from bot.handlers.ai_tools import route_message
from bot.services.scheduler import register_daily_drop_job
from bot.utils.state import get_state   # ensures storage dir is ready

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def _health_check() -> bool:
    ok = True

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        logger.critical("HEALTH CHECK FAILED: OPENAI_API_KEY is not set.")
        ok = False
    else:
        logger.info("HEALTH CHECK OK: OPENAI_API_KEY present (length=%d).", len(api_key))

    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not bot_token:
        logger.critical("HEALTH CHECK FAILED: TELEGRAM_BOT_TOKEN is not set.")
        ok = False
    else:
        logger.info("HEALTH CHECK OK: TELEGRAM_BOT_TOKEN present.")

    import os as _os
    storage_dir = _os.path.join(_os.path.dirname(__file__), "bot", "storage")
    _os.makedirs(storage_dir, exist_ok=True)
    logger.info("HEALTH CHECK OK: storage dir ready at %s.", storage_dir)

    if ok:
        logger.info("BOT READY — all checks passed.")
    return ok


async def post_init(application: Application) -> None:
    register_daily_drop_job(application)


def main() -> None:
    _health_check()

    token = os.environ["TELEGRAM_BOT_TOKEN"]

    app = (
        Application.builder()
        .token(token)
        .post_init(post_init)
        .build()
    )

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))

    # All inline button callbacks
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Global text router — reads persisted state, dispatches to correct AI tool
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_message))

    logger.info("AI Systems Hub — starting polling...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
