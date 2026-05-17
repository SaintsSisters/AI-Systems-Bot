from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.i18n import t
from bot.data.action_workflows import ACTION_WORKFLOWS
from bot.data.action_templates import TEMPLATE_CATEGORIES_RU, TEMPLATE_CATEGORIES_EN, TEMPLATE_KEYS
from bot.data.system_results import SYSTEM_RESULTS
from bot.data.failure_fixes import FAILURE_FIXES


def main_menu_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t("btn_toolbox", lang), callback_data="menu_toolbox"),
            InlineKeyboardButton(t("btn_workflows", lang), callback_data="menu_workflows"),
        ],
        [
            InlineKeyboardButton(t("btn_templates", lang), callback_data="menu_templates"),
            InlineKeyboardButton(t("btn_results", lang), callback_data="menu_results"),
        ],
        [
            InlineKeyboardButton(t("btn_ai_tools", lang), callback_data="menu_ai_tools"),
            InlineKeyboardButton(t("btn_daily_drop", lang), callback_data="menu_drop_settings"),
        ],
        [
            InlineKeyboardButton(t("btn_lessons", lang), callback_data="menu_lessons"),
            InlineKeyboardButton(t("btn_premium", lang), callback_data="menu_premium"),
        ],
        [
            InlineKeyboardButton(t("btn_channel", lang), callback_data="menu_channel"),
        ],
        [
            InlineKeyboardButton(t("switch_lang_btn", lang), callback_data="toggle_lang"),
        ],
    ])


def back_to_main(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")
    ]])


def back_to_drop_settings(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_daily_drop", lang), callback_data="menu_drop_settings")],
        [InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")],
    ])


# ── TOOLBOX ────────────────────────────────────────────────────────────────

def toolbox_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("tool_voice_name", lang), callback_data="tool_voice")],
        [InlineKeyboardButton(t("tool_video_name", lang), callback_data="tool_video")],
        [InlineKeyboardButton(t("tool_automation_name", lang), callback_data="tool_automation")],
        [InlineKeyboardButton(t("tool_content_name", lang), callback_data="tool_content")],
        [InlineKeyboardButton(t("tool_funnel_name", lang), callback_data="tool_funnel")],
        [InlineKeyboardButton(t("tool_post_name", lang), callback_data="tool_post")],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")],
    ])


def tool_result_keyboard(tool_callback: str, lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_regenerate", lang), callback_data=tool_callback)],
        [InlineKeyboardButton(t("btn_all_tools", lang), callback_data="menu_toolbox")],
        [InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")],
    ])


# ── WORKFLOWS ──────────────────────────────────────────────────────────────

def workflows_list_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []
    for i, wf in enumerate(ACTION_WORKFLOWS):
        title = wf["title_ru"] if lang == "ru" else wf["title_en"]
        buttons.append([InlineKeyboardButton(f"{wf['emoji']} {title}", callback_data=f"workflow_{i}")])
    buttons.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def workflow_detail_keyboard(index: int, lang: str = "ru") -> InlineKeyboardMarkup:
    total = len(ACTION_WORKFLOWS)
    buttons = []
    nav = []
    if index > 0:
        nav.append(InlineKeyboardButton(t("btn_prev", lang), callback_data=f"workflow_{index - 1}"))
    if index < total - 1:
        nav.append(InlineKeyboardButton(t("btn_next", lang), callback_data=f"workflow_{index + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton(t("ai_customize_btn", lang), callback_data=f"wf_customize_{index}")])
    buttons.append([InlineKeyboardButton(t("btn_all_workflows", lang), callback_data="menu_workflows")])
    buttons.append([InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def workflow_customized_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_all_workflows", lang), callback_data="menu_workflows")],
        [InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")],
    ])


# ── TEMPLATES ──────────────────────────────────────────────────────────────

def templates_list_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    cats = TEMPLATE_CATEGORIES_RU if lang == "ru" else TEMPLATE_CATEGORIES_EN
    buttons = []
    for i, cat in enumerate(cats):
        buttons.append([InlineKeyboardButton(cat, callback_data=f"tmpl_cat_{i}")])
    buttons.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def template_items_keyboard(cat_index: int, item_index: int, total: int, lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []
    nav = []
    if item_index > 0:
        nav.append(InlineKeyboardButton(t("btn_prev", lang), callback_data=f"tmpl_{cat_index}_{item_index - 1}"))
    if item_index < total - 1:
        nav.append(InlineKeyboardButton(t("btn_next", lang), callback_data=f"tmpl_{cat_index}_{item_index + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton(t("btn_all_templates", lang), callback_data="menu_templates")])
    buttons.append([InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


# ── RESULTS ────────────────────────────────────────────────────────────────

def results_list_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []
    for i, r in enumerate(SYSTEM_RESULTS):
        title = r["title_ru"] if lang == "ru" else r["title_en"]
        buttons.append([InlineKeyboardButton(f"{r['emoji']} {title}", callback_data=f"result_{i}")])
    buttons.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def result_detail_keyboard(index: int, lang: str = "ru") -> InlineKeyboardMarkup:
    total = len(SYSTEM_RESULTS)
    buttons = []
    nav = []
    if index > 0:
        nav.append(InlineKeyboardButton(t("btn_prev", lang), callback_data=f"result_{index - 1}"))
    if index < total - 1:
        nav.append(InlineKeyboardButton(t("btn_next", lang), callback_data=f"result_{index + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton(t("btn_all_results", lang), callback_data="menu_results")])
    buttons.append([InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


# ── AI TOOLS ───────────────────────────────────────────────────────────────

def ai_tools_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("hook_gen_name", lang), callback_data="aitool_hooks")],
        [InlineKeyboardButton(t("cta_gen_name", lang), callback_data="aitool_ctas")],
        [InlineKeyboardButton(t("video_idea_name", lang), callback_data="aitool_videos")],
        [InlineKeyboardButton(t("funnel_idea_name", lang), callback_data="aitool_funnel")],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")],
    ])


def ai_tool_result_keyboard(re_callback: str, lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_regenerate", lang), callback_data=re_callback)],
        [InlineKeyboardButton(t("btn_ai_tools", lang), callback_data="menu_ai_tools")],
        [InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")],
    ])


# ── LESSONS ────────────────────────────────────────────────────────────────

def lessons_list_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []
    for i, lesson in enumerate(FAILURE_FIXES):
        title = lesson["title_ru"] if lang == "ru" else lesson["title_en"]
        buttons.append([InlineKeyboardButton(f"{lesson['emoji']} {title}", callback_data=f"lesson_{i}")])
    buttons.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


def lesson_detail_keyboard(index: int, lang: str = "ru") -> InlineKeyboardMarkup:
    total = len(FAILURE_FIXES)
    buttons = []
    nav = []
    if index > 0:
        nav.append(InlineKeyboardButton(t("btn_prev", lang), callback_data=f"lesson_{index - 1}"))
    if index < total - 1:
        nav.append(InlineKeyboardButton(t("btn_next", lang), callback_data=f"lesson_{index + 1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton(t("btn_all_lessons", lang), callback_data="menu_lessons")])
    buttons.append([InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


# ── DAILY DROP ─────────────────────────────────────────────────────────────

def daily_drop_settings_keyboard(is_subscribed: bool, lang: str = "ru") -> InlineKeyboardMarkup:
    toggle_key = "btn_drop_disable" if is_subscribed else "btn_drop_enable"
    toggle_cb = "drop_unsubscribe" if is_subscribed else "drop_subscribe"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(toggle_key, lang), callback_data=toggle_cb)],
        [InlineKeyboardButton(t("btn_drop_view", lang), callback_data="menu_daily_drop")],
        [InlineKeyboardButton(t("btn_main_menu", lang), callback_data="menu_main")],
    ])


# ── PREMIUM / CHANNEL ──────────────────────────────────────────────────────

def premium_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("premium_btn_waitlist", lang), callback_data="premium_waitlist")],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")],
    ])


def channel_keyboard(lang: str = "ru", channel_url: str = "https://t.me/aisystemshub") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("channel_btn_join", lang), url=channel_url)],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_main")],
    ])
