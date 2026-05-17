from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.data.workflows import WORKFLOWS
from bot.data.toolbox import TOOLBOX_CATEGORIES
from bot.data.templates import TEMPLATE_CATEGORIES
from bot.data.experiments import EXPERIMENTS
from bot.data.lessons import LESSONS


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚙️ Workflows", callback_data="menu_workflows"),
            InlineKeyboardButton("🧰 Toolbox", callback_data="menu_toolbox"),
        ],
        [
            InlineKeyboardButton("📋 Templates", callback_data="menu_templates"),
            InlineKeyboardButton("🧪 Experiments", callback_data="menu_experiments"),
        ],
        [
            InlineKeyboardButton("🤖 AI Tools", callback_data="menu_ai_tools"),
            InlineKeyboardButton("⚡ Daily Drop", callback_data="menu_daily_drop"),
        ],
        [
            InlineKeyboardButton("📚 Lessons", callback_data="menu_lessons"),
            InlineKeyboardButton("👑 Premium", callback_data="menu_premium"),
        ],
        [
            InlineKeyboardButton("📡 Channel", callback_data="menu_channel"),
        ],
    ])


def back_to_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("← Main Menu", callback_data="menu_main")
    ]])


def workflows_list_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for i, wf in enumerate(WORKFLOWS):
        buttons.append([InlineKeyboardButton(
            f"{wf['emoji']} {wf['title']}", callback_data=f"workflow_{i}"
        )])
    buttons.append([InlineKeyboardButton("← Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def workflow_detail_keyboard(index: int) -> InlineKeyboardMarkup:
    buttons = []
    total = len(WORKFLOWS)
    nav = []
    if index > 0:
        nav.append(InlineKeyboardButton("‹ Prev", callback_data=f"workflow_{index - 1}"))
    if index < total - 1:
        nav.append(InlineKeyboardButton("Next ›", callback_data=f"workflow_{index + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton("← All Workflows", callback_data="menu_workflows")])
    buttons.append([InlineKeyboardButton("← Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def toolbox_categories_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    category_emojis = {
        "AI Writing": "✍️",
        "Video Editing": "🎬",
        "Automation": "⚙️",
        "Telegram": "📡",
        "Analytics": "📊",
        "Design": "🎨",
        "Voice AI": "🎙️",
    }
    for i, cat in enumerate(TOOLBOX_CATEGORIES):
        emoji = category_emojis.get(cat, "🔧")
        buttons.append([InlineKeyboardButton(f"{emoji} {cat}", callback_data=f"toolbox_cat_{i}")])
    buttons.append([InlineKeyboardButton("← Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def toolbox_tools_keyboard(cat_index: int, tool_index: int, total_tools: int) -> InlineKeyboardMarkup:
    buttons = []
    nav = []
    if tool_index > 0:
        nav.append(InlineKeyboardButton("‹ Prev", callback_data=f"toolbox_{cat_index}_{tool_index - 1}"))
    if tool_index < total_tools - 1:
        nav.append(InlineKeyboardButton("Next ›", callback_data=f"toolbox_{cat_index}_{tool_index + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton("← Categories", callback_data="menu_toolbox")])
    buttons.append([InlineKeyboardButton("← Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def templates_categories_keyboard() -> InlineKeyboardMarkup:
    category_emojis = {
        "Hook Templates": "🪝",
        "CTA Templates": "📢",
        "Telegram Post Structures": "📡",
        "TikTok/Reels Structures": "🎬",
        "Funnel Structures": "🔁",
        "Viral Opening Patterns": "🚀",
    }
    buttons = []
    for i, cat in enumerate(TEMPLATE_CATEGORIES):
        emoji = category_emojis.get(cat, "📋")
        buttons.append([InlineKeyboardButton(f"{emoji} {cat}", callback_data=f"template_cat_{i}")])
    buttons.append([InlineKeyboardButton("← Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def template_items_keyboard(cat_index: int, item_index: int, total_items: int) -> InlineKeyboardMarkup:
    buttons = []
    nav = []
    if item_index > 0:
        nav.append(InlineKeyboardButton("‹ Prev", callback_data=f"template_{cat_index}_{item_index - 1}"))
    if item_index < total_items - 1:
        nav.append(InlineKeyboardButton("Next ›", callback_data=f"template_{cat_index}_{item_index + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton("← Templates", callback_data="menu_templates")])
    buttons.append([InlineKeyboardButton("← Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def experiments_list_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for i, exp in enumerate(EXPERIMENTS):
        buttons.append([InlineKeyboardButton(
            f"{exp['emoji']} {exp['title']}", callback_data=f"experiment_{i}"
        )])
    buttons.append([InlineKeyboardButton("← Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def experiment_detail_keyboard(index: int) -> InlineKeyboardMarkup:
    buttons = []
    total = len(EXPERIMENTS)
    nav = []
    if index > 0:
        nav.append(InlineKeyboardButton("‹ Prev", callback_data=f"experiment_{index - 1}"))
    if index < total - 1:
        nav.append(InlineKeyboardButton("Next ›", callback_data=f"experiment_{index + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton("← All Experiments", callback_data="menu_experiments")])
    buttons.append([InlineKeyboardButton("← Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def ai_tools_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🪝 Hook Generator", callback_data="aitool_hooks")],
        [InlineKeyboardButton("📢 CTA Generator", callback_data="aitool_ctas")],
        [InlineKeyboardButton("🎬 Video Idea Generator", callback_data="aitool_videos")],
        [InlineKeyboardButton("🔁 Funnel Idea Generator", callback_data="aitool_funnel")],
        [InlineKeyboardButton("← Back", callback_data="menu_main")],
    ])


def lessons_list_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for i, lesson in enumerate(LESSONS):
        buttons.append([InlineKeyboardButton(
            f"{lesson['emoji']} {lesson['title']}", callback_data=f"lesson_{i}"
        )])
    buttons.append([InlineKeyboardButton("← Back", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def lesson_detail_keyboard(index: int) -> InlineKeyboardMarkup:
    buttons = []
    total = len(LESSONS)
    nav = []
    if index > 0:
        nav.append(InlineKeyboardButton("‹ Prev", callback_data=f"lesson_{index - 1}"))
    if index < total - 1:
        nav.append(InlineKeyboardButton("Next ›", callback_data=f"lesson_{index + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton("← All Lessons", callback_data="menu_lessons")])
    buttons.append([InlineKeyboardButton("← Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def premium_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Join Waitlist", callback_data="premium_waitlist")],
        [InlineKeyboardButton("← Back", callback_data="menu_main")],
    ])


def channel_keyboard(channel_url: str = "https://t.me/aisystemshub") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📡 Join Channel", url=channel_url)],
        [InlineKeyboardButton("← Back", callback_data="menu_main")],
    ])


def random_workflow_keyboard(index: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔀 Another Random", callback_data="random_workflow")],
        [InlineKeyboardButton(f"Open Full Workflow", callback_data=f"workflow_{index}")],
        [InlineKeyboardButton("← Main Menu", callback_data="menu_main")],
    ])
