import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.utils.i18n import t
from bot.utils.lang import get_lang, toggle_lang
from bot.utils.storage import track_usage
from bot.services.subscribers import subscribe, unsubscribe, is_subscribed
from bot.data.action_workflows import ACTION_WORKFLOWS
from bot.data.action_templates import ACTION_TEMPLATES, TEMPLATE_KEYS
from bot.data.system_results import SYSTEM_RESULTS
from bot.data.failure_fixes import FAILURE_FIXES
from bot.data.daily_drops import get_daily_drop
from bot.utils.formatting import premium_card, channel_card

from bot.handlers.keyboards import (
    main_menu_keyboard,
    back_to_main,
    back_to_drop_settings,
    toolbox_keyboard,
    workflows_list_keyboard,
    workflow_detail_keyboard,
    workflow_customized_keyboard,
    templates_list_keyboard,
    template_items_keyboard,
    results_list_keyboard,
    result_detail_keyboard,
    ai_tools_keyboard,
    lessons_list_keyboard,
    lesson_detail_keyboard,
    daily_drop_settings_keyboard,
    premium_keyboard,
    channel_keyboard,
)


def _daily_drop_text(drop: dict, lang: str) -> str:
    system = drop["system_ru"] if lang == "ru" else drop["system_en"]
    prompt = drop["prompt_ru"] if lang == "ru" else drop["prompt_en"]
    action = drop["action_ru"] if lang == "ru" else drop["action_en"]
    divider = "─" * 26
    footer = "_Возвращайся завтра за следующим дропом._" if lang == "ru" else "_Come back tomorrow for the next drop._"
    return (
        f"⚡ *{'DAILY DROP' if lang == 'en' else 'DAILY DROP'}*\n"
        f"{divider}\n\n"
        f"🔧 *{'Система' if lang == 'ru' else 'System'}:* {system}\n\n"
        f"📋 *{'Промпт' if lang == 'ru' else 'Prompt'}:*\n{prompt}\n\n"
        f"🎯 *{'Действие' if lang == 'ru' else 'Action'}:*\n{action}\n\n"
        f"{divider}\n{footer}"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    track_usage(user.id, "start")
    lang = get_lang(user.id)
    await update.message.reply_text(
        t("welcome", lang),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard(lang),
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    lang = get_lang(user_id)
    track_usage(user_id, data)

    # ── LANGUAGE TOGGLE ───────────────────────────────────────────────────
    if data == "toggle_lang":
        new_lang = toggle_lang(user_id)
        confirm = t("lang_changed_en", new_lang) if new_lang == "en" else t("lang_changed_ru", new_lang)
        await query.edit_message_text(
            f"{confirm}\n\n{t('welcome', new_lang)}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu_keyboard(new_lang),
        )

    # ── MAIN MENU ─────────────────────────────────────────────────────────
    elif data == "menu_main":
        await query.edit_message_text(
            t("welcome", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu_keyboard(lang),
        )

    # ── TOOLBOX ───────────────────────────────────────────────────────────
    elif data == "menu_toolbox":
        await query.edit_message_text(
            t("toolbox_header", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=toolbox_keyboard(lang),
        )

    # ── WORKFLOWS ─────────────────────────────────────────────────────────
    elif data == "menu_workflows":
        await query.edit_message_text(
            t("workflows_header", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=workflows_list_keyboard(lang),
        )

    elif data.startswith("workflow_") and not data.startswith("workflow_c"):
        index = int(data.split("_")[1])
        wf = ACTION_WORKFLOWS[index]
        template = wf["template_ru"] if lang == "ru" else wf["template_en"]
        await query.edit_message_text(
            template,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=workflow_detail_keyboard(index, lang),
        )

    # ── TEMPLATES ─────────────────────────────────────────────────────────
    elif data == "menu_templates":
        await query.edit_message_text(
            t("templates_header", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=templates_list_keyboard(lang),
        )

    elif data.startswith("tmpl_cat_"):
        cat_index = int(data.split("_")[2])
        key = TEMPLATE_KEYS[cat_index]
        full_key = f"{key}_{lang}"
        cat_data = ACTION_TEMPLATES.get(full_key, ACTION_TEMPLATES.get(f"{key}_ru", {}))
        items = cat_data.get("items", [])
        title = cat_data.get("title", "")
        item_text = f"*{title}*\n\n`{items[0]}`" if items else title
        await query.edit_message_text(
            item_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=template_items_keyboard(cat_index, 0, len(items), lang),
        )

    elif data.startswith("tmpl_") and not data.startswith("tmpl_cat_"):
        parts = data.split("_")
        cat_index = int(parts[1])
        item_index = int(parts[2])
        key = TEMPLATE_KEYS[cat_index]
        full_key = f"{key}_{lang}"
        cat_data = ACTION_TEMPLATES.get(full_key, ACTION_TEMPLATES.get(f"{key}_ru", {}))
        items = cat_data.get("items", [])
        title = cat_data.get("title", "")
        item_text = f"*{title}*\n\n`{items[item_index]}`" if items else title
        await query.edit_message_text(
            item_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=template_items_keyboard(cat_index, item_index, len(items), lang),
        )

    # ── RESULTS ───────────────────────────────────────────────────────────
    elif data == "menu_results":
        await query.edit_message_text(
            t("results_header", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=results_list_keyboard(lang),
        )

    elif data.startswith("result_"):
        index = int(data.split("_")[1])
        r = SYSTEM_RESULTS[index]
        content = r["content_ru"] if lang == "ru" else r["content_en"]
        await query.edit_message_text(
            content,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=result_detail_keyboard(index, lang),
        )

    # ── AI TOOLS ──────────────────────────────────────────────────────────
    elif data == "menu_ai_tools":
        await query.edit_message_text(
            t("ai_tools_header", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tools_keyboard(lang),
        )

    # ── DAILY DROP ────────────────────────────────────────────────────────
    elif data == "menu_drop_settings":
        subscribed = is_subscribed(user_id)
        status = t("drop_active", lang) if subscribed else t("drop_off", lang)
        text = t("drop_settings_header", lang).format(status=status)
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=daily_drop_settings_keyboard(subscribed, lang),
        )

    elif data == "drop_subscribe":
        subscribe(user_id)
        await query.edit_message_text(
            t("drop_enabled_msg", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=daily_drop_settings_keyboard(True, lang),
        )

    elif data == "drop_unsubscribe":
        unsubscribe(user_id)
        await query.edit_message_text(
            t("drop_disabled_msg", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=daily_drop_settings_keyboard(False, lang),
        )

    elif data == "menu_daily_drop":
        drop = get_daily_drop()
        await query.edit_message_text(
            _daily_drop_text(drop, lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_drop_settings(lang),
        )

    # ── LESSONS ───────────────────────────────────────────────────────────
    elif data == "menu_lessons":
        await query.edit_message_text(
            t("lessons_header", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=lessons_list_keyboard(lang),
        )

    elif data.startswith("lesson_"):
        index = int(data.split("_")[1])
        lesson = FAILURE_FIXES[index]
        content = lesson["content_ru"] if lang == "ru" else lesson["content_en"]
        await query.edit_message_text(
            content,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=lesson_detail_keyboard(index, lang),
        )

    # ── PREMIUM / CHANNEL ─────────────────────────────────────────────────
    elif data == "menu_premium":
        await query.edit_message_text(
            premium_card(),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=premium_keyboard(lang),
        )

    elif data == "premium_waitlist":
        await query.edit_message_text(
            t("premium_waitlist_msg", lang),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_main(lang),
        )

    elif data == "menu_channel":
        await query.edit_message_text(
            channel_card(),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=channel_keyboard(lang),
        )
