import logging
import os
import warnings
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

warnings.filterwarnings("ignore", category=UserWarning, module="telegram")

from bot.handlers.menu import start, handle_callback
from bot.handlers.ai_tools import route_message
from bot.services.scheduler import register_daily_drop_job

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    register_daily_drop_job(application)


def main() -> None:
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

    # Global text message router — dispatches based on persisted user state
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_message))

    logger.info("AI Systems Hub — Execution Engine starting...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
