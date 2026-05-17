import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.handlers.keyboards import (
    main_menu_keyboard,
    workflows_list_keyboard,
    workflow_detail_keyboard,
    toolbox_categories_keyboard,
    toolbox_tools_keyboard,
    templates_categories_keyboard,
    template_items_keyboard,
    experiments_list_keyboard,
    experiment_detail_keyboard,
    ai_tools_keyboard,
    lessons_list_keyboard,
    lesson_detail_keyboard,
    premium_keyboard,
    channel_keyboard,
    back_to_main,
    random_workflow_keyboard,
    daily_drop_settings_keyboard,
    back_to_drop_settings,
)
from bot.services.subscribers import subscribe, unsubscribe, is_subscribed
from bot.utils.formatting import (
    workflow_card,
    tool_card,
    template_card,
    experiment_card,
    lesson_card,
    daily_drop_card,
    premium_card,
    channel_card,
)
from bot.data.workflows import WORKFLOWS
from bot.data.toolbox import TOOLBOX, TOOLBOX_CATEGORIES
from bot.data.templates import TEMPLATES, TEMPLATE_CATEGORIES
from bot.data.experiments import EXPERIMENTS
from bot.data.lessons import LESSONS
from bot.data.daily_drops import get_daily_drop
from bot.utils.storage import track_usage

WELCOME_TEXT = """⚡ *AI SYSTEMS HUB*

Your digital operating system for:
→ AI workflows & automation
→ Content pipelines
→ Telegram growth systems
→ Traffic funnels
→ Practical experiments

Built for creators, marketers, and builders who move fast.

*What do you want to explore?*"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    track_usage(user.id, "start")
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard(),
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    track_usage(user_id, data)

    if data == "menu_main":
        await query.edit_message_text(
            WELCOME_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu_keyboard(),
        )

    elif data == "menu_workflows":
        text = "⚙️ *WORKFLOWS*\n\nReady-to-use digital system blueprints.\nChoose a workflow to explore:"
        await query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=workflows_list_keyboard()
        )

    elif data.startswith("workflow_"):
        index = int(data.split("_")[1])
        wf = WORKFLOWS[index]
        await query.edit_message_text(
            workflow_card(wf),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=workflow_detail_keyboard(index),
        )

    elif data == "random_workflow":
        index = random.randint(0, len(WORKFLOWS) - 1)
        wf = WORKFLOWS[index]
        text = f"🔀 *RANDOM WORKFLOW*\n\n{workflow_card(wf)}"
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=random_workflow_keyboard(index),
        )

    elif data == "menu_toolbox":
        text = "🧰 *TOOLBOX*\n\nCurated AI and automation tools by category.\nChoose a category:"
        await query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=toolbox_categories_keyboard()
        )

    elif data.startswith("toolbox_cat_"):
        cat_index = int(data.split("_")[2])
        cat_name = TOOLBOX_CATEGORIES[cat_index]
        tools = TOOLBOX[cat_name]
        tool = tools[0]
        await query.edit_message_text(
            tool_card(tool),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=toolbox_tools_keyboard(cat_index, 0, len(tools)),
        )

    elif data.startswith("toolbox_") and not data.startswith("toolbox_cat_"):
        parts = data.split("_")
        cat_index = int(parts[1])
        tool_index = int(parts[2])
        cat_name = TOOLBOX_CATEGORIES[cat_index]
        tools = TOOLBOX[cat_name]
        tool = tools[tool_index]
        await query.edit_message_text(
            tool_card(tool),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=toolbox_tools_keyboard(cat_index, tool_index, len(tools)),
        )

    elif data == "menu_templates":
        text = "📋 *TEMPLATES*\n\nReusable structures for content and funnels.\nChoose a category:"
        await query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=templates_categories_keyboard()
        )

    elif data.startswith("template_cat_"):
        cat_index = int(data.split("_")[2])
        cat_name = TEMPLATE_CATEGORIES[cat_index]
        items = TEMPLATES[cat_name]
        item = items[0]
        await query.edit_message_text(
            template_card(item),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=template_items_keyboard(cat_index, 0, len(items)),
        )

    elif data.startswith("template_") and not data.startswith("template_cat_"):
        parts = data.split("_")
        cat_index = int(parts[1])
        item_index = int(parts[2])
        cat_name = TEMPLATE_CATEGORIES[cat_index]
        items = TEMPLATES[cat_name]
        item = items[item_index]
        await query.edit_message_text(
            template_card(item),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=template_items_keyboard(cat_index, item_index, len(items)),
        )

    elif data == "menu_experiments":
        text = "🧪 *EXPERIMENTS*\n\nReal growth and content experiments — building in public.\nChoose an experiment:"
        await query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=experiments_list_keyboard()
        )

    elif data.startswith("experiment_"):
        index = int(data.split("_")[1])
        exp = EXPERIMENTS[index]
        await query.edit_message_text(
            experiment_card(exp),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=experiment_detail_keyboard(index),
        )

    elif data == "menu_ai_tools":
        text = "🤖 *AI TOOLS*\n\nMini AI utilities. Choose a tool:"
        await query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=ai_tools_keyboard()
        )

    elif data == "menu_drop_settings":
        subscribed = is_subscribed(user_id)
        status_line = "✅ *Active* — you'll receive a drop at 18:00 UTC daily." if subscribed else "○ *Off* — enable to receive a daily drop at 18:00 UTC."
        text = (
            f"⚡ *DAILY DROP SETTINGS*\n\n"
            f"One practical insight, one action, delivered once per day.\n\n"
            f"Status: {status_line}\n\n"
            f"No spam. One message per day. Unsubscribe anytime."
        )
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=daily_drop_settings_keyboard(subscribed),
        )

    elif data == "drop_subscribe":
        subscribe(user_id)
        track_usage(user_id, "drop_subscribe")
        text = (
            "🔔 *Daily Drop enabled.*\n\n"
            "You'll receive one drop per day at 18:00 UTC.\n"
            "One insight. One action. Nothing else.\n\n"
            "You can disable it here anytime."
        )
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=daily_drop_settings_keyboard(True),
        )

    elif data == "drop_unsubscribe":
        unsubscribe(user_id)
        track_usage(user_id, "drop_unsubscribe")
        text = (
            "🔕 *Daily Drop disabled.*\n\n"
            "You won't receive any more scheduled drops.\n"
            "You can re-enable it here anytime."
        )
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=daily_drop_settings_keyboard(False),
        )

    elif data == "menu_daily_drop":
        drop = get_daily_drop()
        await query.edit_message_text(
            daily_drop_card(drop),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_drop_settings(),
        )

    elif data == "menu_lessons":
        text = "📚 *LESSONS*\n\nHonest breakdowns of failures and practical insights.\nChoose a lesson:"
        await query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=lessons_list_keyboard()
        )

    elif data.startswith("lesson_"):
        index = int(data.split("_")[1])
        lesson = LESSONS[index]
        await query.edit_message_text(
            lesson_card(lesson),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=lesson_detail_keyboard(index),
        )

    elif data == "menu_premium":
        await query.edit_message_text(
            premium_card(),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=premium_keyboard(),
        )

    elif data == "premium_waitlist":
        await query.edit_message_text(
            "🔔 *WAITLIST*\n\nYou're on the list. We'll notify you when Premium launches with early-access pricing.\n\nIn the meantime, explore everything in the free tier — there's a lot here.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_main(),
        )

    elif data == "menu_channel":
        await query.edit_message_text(
            channel_card(),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=channel_keyboard(),
        )
