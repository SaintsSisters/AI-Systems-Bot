"""
All AI tool logic.
No ConversationHandlers — state is persisted in bot/storage/user_state.json.
Entry points set state; the global message router dispatches here.
"""
from telegram import Update, Message
from telegram.constants import ParseMode

from bot.utils.i18n import t
from bot.utils.lang import get_lang
from bot.utils.state import get_state, set_state, reset_state, store_data, advance_step
from bot.utils.storage import track_usage
from bot.services.openai_service import generate_hooks, generate_ctas, generate_video_ideas, generate_funnel_idea
from bot.services.action_service import (
    gen_voice_script, gen_video_script, gen_automation,
    gen_content_pack, gen_funnel, gen_telegram_post, gen_workflow_customized,
)
from bot.handlers.keyboards import tool_result_keyboard, ai_tool_result_keyboard, workflow_customized_keyboard
from bot.data.action_workflows import ACTION_WORKFLOWS


# ── Helpers ────────────────────────────────────────────────────────────────

async def _thinking(message: Message, key: str, lang: str) -> Message:
    return await message.reply_text(t(key, lang))


async def _safe_error(message: Message, lang: str) -> None:
    await message.reply_text(t("error_msg", lang))


# ══════════════════════════════════════════════════════════════════════════
# ENTRY POINTS — called from menu.handle_callback when a tool button is tapped
# Each sets state and sends the input-prompt message.
# ══════════════════════════════════════════════════════════════════════════

async def enter_voice(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "voice", True)
    await query.edit_message_text(t("voice_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_video(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "video", True)
    await query.edit_message_text(t("video_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_automation(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "automation", True)
    await query.edit_message_text(t("automation_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_content(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "content", True)
    await query.edit_message_text(t("content_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_funnel(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "funnel", True)
    await query.edit_message_text(t("funnel_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_post(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "post", True)
    await query.edit_message_text(t("post_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_wf_customize(update: Update, wf_index: int) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "wf_customize", True, extra={"wf_index": wf_index})
    await query.edit_message_text(t("customize_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_hooks(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "hooks", True, step=1)
    await query.edit_message_text(t("hook_ask1", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_ctas(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "ctas", True, step=1)
    await query.edit_message_text(t("cta_ask1", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_video_ideas(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "video_ideas", True)
    await query.edit_message_text(t("videoidea_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_funnel_ideas(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "funnel_ideas", True)
    await query.edit_message_text(t("funnelidea_ask", lang), parse_mode=ParseMode.MARKDOWN)


# ══════════════════════════════════════════════════════════════════════════
# MESSAGE HANDLERS — called by the global router with user's text input
# Each generates AI output and resets state.
# ══════════════════════════════════════════════════════════════════════════

async def handle_voice(update: Update) -> None:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_voice")
    msg = await _thinking(update.message, "voice_thinking", lang)
    try:
        result = await gen_voice_script(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("voice_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_voice", lang),
        )
    except Exception:
        await msg.delete()
        await _safe_error(update.message, lang)
    finally:
        reset_state(update.effective_user.id)


async def handle_video(update: Update) -> None:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_video")
    msg = await _thinking(update.message, "video_thinking", lang)
    try:
        result = await gen_video_script(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("video_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_video", lang),
        )
    except Exception:
        await msg.delete()
        await _safe_error(update.message, lang)
    finally:
        reset_state(update.effective_user.id)


async def handle_automation(update: Update) -> None:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_automation")
    msg = await _thinking(update.message, "automation_thinking", lang)
    try:
        result = await gen_automation(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("automation_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_automation", lang),
        )
    except Exception:
        await msg.delete()
        await _safe_error(update.message, lang)
    finally:
        reset_state(update.effective_user.id)


async def handle_content(update: Update) -> None:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_content")
    msg = await _thinking(update.message, "content_thinking", lang)
    try:
        result = await gen_content_pack(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("content_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_content", lang),
        )
    except Exception:
        await msg.delete()
        await _safe_error(update.message, lang)
    finally:
        reset_state(update.effective_user.id)


async def handle_funnel(update: Update) -> None:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_funnel")
    msg = await _thinking(update.message, "funnel_thinking", lang)
    try:
        result = await gen_funnel(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("funnel_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_funnel", lang),
        )
    except Exception:
        await msg.delete()
        await _safe_error(update.message, lang)
    finally:
        reset_state(update.effective_user.id)


async def handle_post(update: Update) -> None:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_post")
    msg = await _thinking(update.message, "post_thinking", lang)
    try:
        result = await gen_telegram_post(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("post_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_post", lang),
        )
    except Exception:
        await msg.delete()
        await _safe_error(update.message, lang)
    finally:
        reset_state(update.effective_user.id)


async def handle_wf_customize(update: Update, state: dict) -> None:
    lang = get_lang(update.effective_user.id)
    wf_index = state.get("data", {}).get("wf_index", 0)
    wf = ACTION_WORKFLOWS[wf_index]
    wf_name = wf["title_ru"] if lang == "ru" else wf["title_en"]
    msg = await update.message.reply_text(t("customize_thinking", lang))
    try:
        result = await gen_workflow_customized(wf_name, update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            f"⚙️ *{wf_name}*\n\n{result}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=workflow_customized_keyboard(lang),
        )
    except Exception:
        await msg.delete()
        await _safe_error(update.message, lang)
    finally:
        reset_state(update.effective_user.id)


# ── Multi-step: Hooks ──────────────────────────────────────────────────────

async def handle_hooks(update: Update, state: dict) -> None:
    lang = get_lang(update.effective_user.id)
    step = state.get("step", 1)

    if step == 1:
        store_data(update.effective_user.id, "niche", update.message.text)
        advance_step(update.effective_user.id)
        await update.message.reply_text(t("hook_ask2", lang), parse_mode=ParseMode.MARKDOWN)

    elif step == 2:
        niche = state.get("data", {}).get("niche", "")
        track_usage(update.effective_user.id, "hook_generator")
        msg = await _thinking(update.message, "hook_thinking", lang)
        try:
            result = await generate_hooks(niche, update.message.text)
            await msg.delete()
            await update.message.reply_text(
                t("hook_result_header", lang) + result,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=ai_tool_result_keyboard("aitool_hooks", lang),
            )
        except Exception:
            await msg.delete()
            await _safe_error(update.message, lang)
        finally:
            reset_state(update.effective_user.id)


# ── Multi-step: CTAs ───────────────────────────────────────────────────────

async def handle_ctas(update: Update, state: dict) -> None:
    lang = get_lang(update.effective_user.id)
    step = state.get("step", 1)

    if step == 1:
        store_data(update.effective_user.id, "platform", update.message.text)
        advance_step(update.effective_user.id)
        await update.message.reply_text(t("cta_ask2", lang), parse_mode=ParseMode.MARKDOWN)

    elif step == 2:
        platform = state.get("data", {}).get("platform", "")
        track_usage(update.effective_user.id, "cta_generator")
        msg = await _thinking(update.message, "cta_thinking", lang)
        try:
            result = await generate_ctas(platform, update.message.text)
            await msg.delete()
            await update.message.reply_text(
                t("cta_result_header", lang) + result,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=ai_tool_result_keyboard("aitool_ctas", lang),
            )
        except Exception:
            await msg.delete()
            await _safe_error(update.message, lang)
        finally:
            reset_state(update.effective_user.id)


# ── Single-step: Video Ideas ───────────────────────────────────────────────

async def handle_video_ideas(update: Update) -> None:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "video_generator")
    msg = await _thinking(update.message, "videoidea_thinking", lang)
    try:
        result = await generate_video_ideas(update.message.text)
        await msg.delete()
        await update.message.reply_text(
            t("videoidea_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_videos", lang),
        )
    except Exception:
        await msg.delete()
        await _safe_error(update.message, lang)
    finally:
        reset_state(update.effective_user.id)


# ── Single-step: Funnel Ideas ──────────────────────────────────────────────

async def handle_funnel_ideas(update: Update) -> None:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "funnel_generator")
    msg = await _thinking(update.message, "funnelidea_thinking", lang)
    try:
        result = await generate_funnel_idea(update.message.text)
        await msg.delete()
        await update.message.reply_text(
            t("funnelidea_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_funnel", lang),
        )
    except Exception:
        await msg.delete()
        await _safe_error(update.message, lang)
    finally:
        reset_state(update.effective_user.id)


# ══════════════════════════════════════════════════════════════════════════
# GLOBAL MESSAGE ROUTER
# Called from main.py for every non-command text message.
# ══════════════════════════════════════════════════════════════════════════

TOOL_DISPATCH = {
    "voice":        handle_voice,
    "video":        handle_video,
    "automation":   handle_automation,
    "content":      handle_content,
    "funnel":       handle_funnel,
    "post":         handle_post,
    "video_ideas":  handle_video_ideas,
    "funnel_ideas": handle_funnel_ideas,
}

MULTI_STEP_DISPATCH = {
    "hooks":        handle_hooks,
    "ctas":         handle_ctas,
    "wf_customize": handle_wf_customize,
}


async def route_message(update: Update, _) -> None:
    """Global text-message router — checks persisted state and dispatches."""
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    state = get_state(user_id)

    if not state.get("awaiting_input"):
        # No active tool — show friendly nudge
        nudge = (
            "Выбери инструмент через меню или нажми /start"
            if lang == "ru"
            else "Choose a tool from the menu or press /start"
        )
        await update.message.reply_text(nudge)
        return

    tool = state.get("active_tool")

    # Single-step tools
    if tool in TOOL_DISPATCH:
        await TOOL_DISPATCH[tool](update)
        return

    # Multi-step tools (need state passed in)
    if tool in MULTI_STEP_DISPATCH:
        await MULTI_STEP_DISPATCH[tool](update, state)
        return

    # Unknown tool — safe reset
    reset_state(user_id)
    nudge = (
        "Что-то пошло не так. Выбери инструмент через /start"
        if lang == "ru"
        else "Something went wrong. Choose a tool via /start"
    )
    await update.message.reply_text(nudge)
