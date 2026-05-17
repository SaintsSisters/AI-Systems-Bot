import logging
import os
import warnings
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

warnings.filterwarnings("ignore", category=UserWarning, module="telegram")

from bot.handlers.menu import start, handle_callback
from bot.handlers.ai_tools import get_ai_tool_conversations

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = Application.builder().token(token).build()

    for conv in get_ai_tool_conversations():
        app.add_handler(conv)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    logger.info("AI Systems Hub bot starting...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
