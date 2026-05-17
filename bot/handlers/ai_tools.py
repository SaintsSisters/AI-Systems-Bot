"""
AI tool logic — state-based routing, no ConversationHandlers.
All errors are logged with full traceback. Nothing is silently swallowed.
"""
import logging
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

logger = logging.getLogger(__name__)

ERROR_RU = "❌ Ошибка генерации. Попробуйте ещё раз или выберите другой инструмент."
ERROR_EN = "❌ Generation error. Please try again or choose another tool."


def _error_text(lang: str) -> str:
    return ERROR_RU if lang == "ru" else ERROR_EN


# ── Safe "thinking" message ────────────────────────────────────────────────

async def _send_thinking(message: Message, key: str, lang: str) -> Message:
    return await message.reply_text(t(key, lang))


async def _try_delete(msg: Message) -> None:
    """Delete a message, ignoring errors (already deleted, etc.)."""
    try:
        await msg.delete()
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════════════
# ENTRY POINTS — save state to disk and ask for user input
# ══════════════════════════════════════════════════════════════════════════

async def enter_voice(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "voice", True)
    logger.info("User %d entered tool: voice", query.from_user.id)
    await query.edit_message_text(t("voice_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_video(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "video", True)
    logger.info("User %d entered tool: video", query.from_user.id)
    await query.edit_message_text(t("video_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_automation(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "automation", True)
    logger.info("User %d entered tool: automation", query.from_user.id)
    await query.edit_message_text(t("automation_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_content(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "content", True)
    logger.info("User %d entered tool: content", query.from_user.id)
    await query.edit_message_text(t("content_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_funnel(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "funnel", True)
    logger.info("User %d entered tool: funnel", query.from_user.id)
    await query.edit_message_text(t("funnel_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_post(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "post", True)
    logger.info("User %d entered tool: post", query.from_user.id)
    await query.edit_message_text(t("post_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_wf_customize(update: Update, wf_index: int) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "wf_customize", True, extra={"wf_index": wf_index})
    logger.info("User %d entered tool: wf_customize (index=%d)", query.from_user.id, wf_index)
    await query.edit_message_text(t("customize_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_hooks(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "hooks", True, step=1)
    logger.info("User %d entered tool: hooks step 1", query.from_user.id)
    await query.edit_message_text(t("hook_ask1", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_ctas(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "ctas", True, step=1)
    logger.info("User %d entered tool: ctas step 1", query.from_user.id)
    await query.edit_message_text(t("cta_ask1", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_video_ideas(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "video_ideas", True)
    logger.info("User %d entered tool: video_ideas", query.from_user.id)
    await query.edit_message_text(t("videoidea_ask", lang), parse_mode=ParseMode.MARKDOWN)


async def enter_funnel_ideas(update: Update) -> None:
    query = update.callback_query
    lang = get_lang(query.from_user.id)
    set_state(query.from_user.id, "funnel_ideas", True)
    logger.info("User %d entered tool: funnel_ideas", query.from_user.id)
    await query.edit_message_text(t("funnelidea_ask", lang), parse_mode=ParseMode.MARKDOWN)


# ══════════════════════════════════════════════════════════════════════════
# AI GENERATION HANDLERS — each calls OpenAI, logs result, resets state
# ══════════════════════════════════════════════════════════════════════════

async def handle_voice(update: Update) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    track_usage(user_id, "tool_voice")
    thinking = await _send_thinking(update.message, "voice_thinking", lang)
    try:
        result = await gen_voice_script(update.message.text, lang)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("voice_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_voice", lang),
        )
        logger.info("User %d: voice script delivered.", user_id)
    except Exception as e:
        logger.error("User %d: voice script FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


async def handle_video(update: Update) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    track_usage(user_id, "tool_video")
    thinking = await _send_thinking(update.message, "video_thinking", lang)
    try:
        result = await gen_video_script(update.message.text, lang)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("video_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_video", lang),
        )
        logger.info("User %d: video script delivered.", user_id)
    except Exception as e:
        logger.error("User %d: video script FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


async def handle_automation(update: Update) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    track_usage(user_id, "tool_automation")
    thinking = await _send_thinking(update.message, "automation_thinking", lang)
    try:
        result = await gen_automation(update.message.text, lang)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("automation_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_automation", lang),
        )
        logger.info("User %d: automation delivered.", user_id)
    except Exception as e:
        logger.error("User %d: automation FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


async def handle_content(update: Update) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    track_usage(user_id, "tool_content")
    thinking = await _send_thinking(update.message, "content_thinking", lang)
    try:
        result = await gen_content_pack(update.message.text, lang)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("content_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_content", lang),
        )
        logger.info("User %d: content pack delivered.", user_id)
    except Exception as e:
        logger.error("User %d: content pack FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


async def handle_funnel(update: Update) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    track_usage(user_id, "tool_funnel")
    thinking = await _send_thinking(update.message, "funnel_thinking", lang)
    try:
        result = await gen_funnel(update.message.text, lang)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("funnel_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_funnel", lang),
        )
        logger.info("User %d: funnel delivered.", user_id)
    except Exception as e:
        logger.error("User %d: funnel FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


async def handle_post(update: Update) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    track_usage(user_id, "tool_post")
    thinking = await _send_thinking(update.message, "post_thinking", lang)
    try:
        result = await gen_telegram_post(update.message.text, lang)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("post_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_post", lang),
        )
        logger.info("User %d: telegram post delivered.", user_id)
    except Exception as e:
        logger.error("User %d: telegram post FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


async def handle_wf_customize(update: Update, state: dict) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    wf_index = state.get("data", {}).get("wf_index", 0)
    wf = ACTION_WORKFLOWS[wf_index]
    wf_name = wf["title_ru"] if lang == "ru" else wf["title_en"]
    thinking = await update.message.reply_text(t("customize_thinking", lang))
    try:
        result = await gen_workflow_customized(wf_name, update.message.text, lang)
        await _try_delete(thinking)
        await update.message.reply_text(
            f"⚙️ *{wf_name}*\n\n{result}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=workflow_customized_keyboard(lang),
        )
        logger.info("User %d: workflow customize delivered.", user_id)
    except Exception as e:
        logger.error("User %d: wf_customize FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


# ── Multi-step: Hooks ──────────────────────────────────────────────────────

async def handle_hooks(update: Update, state: dict) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    step = state.get("step", 1)

    if step == 1:
        store_data(user_id, "niche", update.message.text)
        advance_step(user_id)
        logger.info("User %d: hooks step 1 done, niche saved, asking step 2.", user_id)
        await update.message.reply_text(t("hook_ask2", lang), parse_mode=ParseMode.MARKDOWN)
        return

    # step 2 — generate
    niche = state.get("data", {}).get("niche", "")
    audience = update.message.text
    track_usage(user_id, "hook_generator")
    logger.info("User %d: hooks generating (niche=%s, audience=%s).", user_id, niche, audience)
    thinking = await _send_thinking(update.message, "hook_thinking", lang)
    try:
        result = await generate_hooks(niche, audience)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("hook_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_hooks", lang),
        )
        logger.info("User %d: hooks delivered.", user_id)
    except Exception as e:
        logger.error("User %d: hooks FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


# ── Multi-step: CTAs ───────────────────────────────────────────────────────

async def handle_ctas(update: Update, state: dict) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    step = state.get("step", 1)

    if step == 1:
        store_data(user_id, "platform", update.message.text)
        advance_step(user_id)
        logger.info("User %d: ctas step 1 done, platform saved, asking step 2.", user_id)
        await update.message.reply_text(t("cta_ask2", lang), parse_mode=ParseMode.MARKDOWN)
        return

    # step 2 — generate
    platform = state.get("data", {}).get("platform", "")
    goal = update.message.text
    track_usage(user_id, "cta_generator")
    logger.info("User %d: ctas generating (platform=%s, goal=%s).", user_id, platform, goal)
    thinking = await _send_thinking(update.message, "cta_thinking", lang)
    try:
        result = await generate_ctas(platform, goal)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("cta_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_ctas", lang),
        )
        logger.info("User %d: ctas delivered.", user_id)
    except Exception as e:
        logger.error("User %d: ctas FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


# ── Single-step: Video Ideas ───────────────────────────────────────────────

async def handle_video_ideas(update: Update) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    track_usage(user_id, "video_generator")
    logger.info("User %d: video_ideas generating.", user_id)
    thinking = await _send_thinking(update.message, "videoidea_thinking", lang)
    try:
        result = await generate_video_ideas(update.message.text)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("videoidea_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_videos", lang),
        )
        logger.info("User %d: video_ideas delivered.", user_id)
    except Exception as e:
        logger.error("User %d: video_ideas FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


# ── Single-step: Funnel Ideas ──────────────────────────────────────────────

async def handle_funnel_ideas(update: Update) -> None:
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    track_usage(user_id, "funnel_generator")
    logger.info("User %d: funnel_ideas generating.", user_id)
    thinking = await _send_thinking(update.message, "funnelidea_thinking", lang)
    try:
        result = await generate_funnel_idea(update.message.text)
        await _try_delete(thinking)
        await update.message.reply_text(
            t("funnelidea_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_funnel", lang),
        )
        logger.info("User %d: funnel_ideas delivered.", user_id)
    except Exception as e:
        logger.error("User %d: funnel_ideas FAILED — %s", user_id, e, exc_info=True)
        await _try_delete(thinking)
        await update.message.reply_text(_error_text(lang))
    finally:
        reset_state(user_id)


# ══════════════════════════════════════════════════════════════════════════
# GLOBAL MESSAGE ROUTER
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
    """Reads persisted state and dispatches text to the correct tool handler."""
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    state = get_state(user_id)
    tool = state.get("active_tool")
    awaiting = state.get("awaiting_input", False)

    logger.info(
        "route_message: user=%d awaiting=%s tool=%s text=%r",
        user_id, awaiting, tool, update.message.text[:60] if update.message.text else "",
    )

    if not awaiting or not tool:
        nudge = (
            "Выбери инструмент через меню или нажми /start"
            if lang == "ru"
            else "Choose a tool from the menu or press /start"
        )
        await update.message.reply_text(nudge)
        return

    if tool in TOOL_DISPATCH:
        await TOOL_DISPATCH[tool](update)
        return

    if tool in MULTI_STEP_DISPATCH:
        await MULTI_STEP_DISPATCH[tool](update, state)
        return

    # Unknown tool name in state — safe recovery
    logger.warning("route_message: unknown tool=%s for user=%d — resetting state.", tool, user_id)
    reset_state(user_id)
    await update.message.reply_text(
        "Что-то пошло не так. Нажми /start чтобы вернуться в меню."
        if lang == "ru"
        else "Something went wrong. Press /start to return to the menu."
    )
