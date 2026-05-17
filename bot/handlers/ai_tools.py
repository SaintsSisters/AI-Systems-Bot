from telegram import Update
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, filters, CallbackQueryHandler,
)
from telegram.constants import ParseMode

from bot.utils.i18n import t
from bot.utils.lang import get_lang
from bot.utils.storage import track_usage
from bot.services.openai_service import generate_hooks, generate_ctas, generate_video_ideas, generate_funnel_idea
from bot.services.action_service import (
    gen_voice_script, gen_video_script, gen_automation,
    gen_content_pack, gen_funnel, gen_telegram_post, gen_workflow_customized,
)
from bot.handlers.keyboards import tool_result_keyboard, ai_tool_result_keyboard, workflow_customized_keyboard
from bot.data.action_workflows import ACTION_WORKFLOWS

# ── States ─────────────────────────────────────────────────────────────────
VOICE_INPUT      = 1
VIDEO_INPUT      = 2
AUTOMATION_INPUT = 3
CONTENT_INPUT    = 4
FUNNEL_INPUT     = 5
POST_INPUT       = 6
WF_CUSTOMIZE     = 7

HOOK_NICHE, HOOK_AUDIENCE = 10, 11
CTA_PLATFORM, CTA_GOAL   = 20, 21
VIDEO_NICHE_S            = 30
FUNNEL_NICHE_S           = 40


# ── Helpers ────────────────────────────────────────────────────────────────

async def _thinking(update: Update, key: str, lang: str):
    return await update.message.reply_text(t(key, lang))


async def _error(update: Update, lang: str):
    await update.message.reply_text(t("error_msg", lang))


# ══════════════════════════════════════════════════════════════════════════
# TOOLBOX ACTION GENERATORS
# ══════════════════════════════════════════════════════════════════════════

async def start_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("voice_ask", lang), parse_mode=ParseMode.MARKDOWN)
    return VOICE_INPUT


async def voice_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_voice")
    msg = await _thinking(update, "voice_thinking", lang)
    try:
        result = await gen_voice_script(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("voice_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_voice", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


async def start_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("video_ask", lang), parse_mode=ParseMode.MARKDOWN)
    return VIDEO_INPUT


async def video_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_video")
    msg = await _thinking(update, "video_thinking", lang)
    try:
        result = await gen_video_script(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("video_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_video", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


async def start_automation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("automation_ask", lang), parse_mode=ParseMode.MARKDOWN)
    return AUTOMATION_INPUT


async def automation_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_automation")
    msg = await _thinking(update, "automation_thinking", lang)
    try:
        result = await gen_automation(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("automation_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_automation", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


async def start_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("content_ask", lang), parse_mode=ParseMode.MARKDOWN)
    return CONTENT_INPUT


async def content_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_content")
    msg = await _thinking(update, "content_thinking", lang)
    try:
        result = await gen_content_pack(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("content_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_content", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


async def start_funnel_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("funnel_ask", lang), parse_mode=ParseMode.MARKDOWN)
    return FUNNEL_INPUT


async def funnel_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_funnel")
    msg = await _thinking(update, "funnel_thinking", lang)
    try:
        result = await gen_funnel(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("funnel_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_funnel", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


async def start_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("post_ask", lang), parse_mode=ParseMode.MARKDOWN)
    return POST_INPUT


async def post_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "tool_post")
    msg = await _thinking(update, "post_thinking", lang)
    try:
        result = await gen_telegram_post(update.message.text, lang)
        await msg.delete()
        await update.message.reply_text(
            t("post_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=tool_result_keyboard("tool_post", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


# ══════════════════════════════════════════════════════════════════════════
# WORKFLOW CUSTOMIZER
# ══════════════════════════════════════════════════════════════════════════

async def start_wf_customize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    wf_index = int(query.data.split("_")[2])
    context.user_data["wf_customize_index"] = wf_index
    await query.edit_message_text(
        t("customize_ask", lang),
        parse_mode=ParseMode.MARKDOWN,
    )
    return WF_CUSTOMIZE


async def wf_customize_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    wf_index = context.user_data.get("wf_customize_index", 0)
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
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


# ══════════════════════════════════════════════════════════════════════════
# AI TOOLS (existing 4 — now bilingual)
# ══════════════════════════════════════════════════════════════════════════

async def start_hook_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("hook_ask1", lang), parse_mode=ParseMode.MARKDOWN)
    return HOOK_NICHE


async def hook_niche_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["hook_niche"] = update.message.text
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(t("hook_ask2", lang), parse_mode=ParseMode.MARKDOWN)
    return HOOK_AUDIENCE


async def hook_audience_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    niche = context.user_data.get("hook_niche", "")
    track_usage(update.effective_user.id, "hook_generator")
    msg = await update.message.reply_text(t("hook_thinking", lang))
    try:
        result = await generate_hooks(niche, update.message.text)
        await msg.delete()
        await update.message.reply_text(
            t("hook_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_hooks", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


async def start_cta_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("cta_ask1", lang), parse_mode=ParseMode.MARKDOWN)
    return CTA_PLATFORM


async def cta_platform_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["cta_platform"] = update.message.text
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(t("cta_ask2", lang), parse_mode=ParseMode.MARKDOWN)
    return CTA_GOAL


async def cta_goal_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    platform = context.user_data.get("cta_platform", "")
    track_usage(update.effective_user.id, "cta_generator")
    msg = await update.message.reply_text(t("cta_thinking", lang))
    try:
        result = await generate_ctas(platform, update.message.text)
        await msg.delete()
        await update.message.reply_text(
            t("cta_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_ctas", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


async def start_video_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("videoidea_ask", lang), parse_mode=ParseMode.MARKDOWN)
    return VIDEO_NICHE_S


async def video_niche_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "video_generator")
    msg = await update.message.reply_text(t("videoidea_thinking", lang))
    try:
        result = await generate_video_ideas(update.message.text)
        await msg.delete()
        await update.message.reply_text(
            t("videoidea_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_videos", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


async def start_funnel_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    await query.edit_message_text(t("funnelidea_ask", lang), parse_mode=ParseMode.MARKDOWN)
    return FUNNEL_NICHE_S


async def funnel_niche_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    track_usage(update.effective_user.id, "funnel_generator")
    msg = await update.message.reply_text(t("funnelidea_thinking", lang))
    try:
        result = await generate_funnel_idea(update.message.text)
        await msg.delete()
        await update.message.reply_text(
            t("funnelidea_result_header", lang) + result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ai_tool_result_keyboard("aitool_funnel", lang),
        )
    except Exception:
        await msg.edit_text(t("error_msg", lang))
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(t("cancel_msg", lang))
    return ConversationHandler.END


# ══════════════════════════════════════════════════════════════════════════
# REGISTER ALL CONVERSATIONS
# ══════════════════════════════════════════════════════════════════════════

def get_all_conversations():
    cancel_h = CommandHandler("cancel", cancel)

    def _make(entry_pattern, state_id, input_handler, **kwargs):
        return ConversationHandler(
            entry_points=[CallbackQueryHandler(kwargs["entry_fn"], pattern=f"^{entry_pattern}$")],
            states={state_id: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_handler)]},
            fallbacks=[cancel_h],
            per_chat=True, per_user=True, per_message=False,
        )

    voice_conv = _make("tool_voice", VOICE_INPUT, voice_received, entry_fn=start_voice)
    video_conv = _make("tool_video", VIDEO_INPUT, video_received, entry_fn=start_video)
    auto_conv  = _make("tool_automation", AUTOMATION_INPUT, automation_received, entry_fn=start_automation)
    content_conv = _make("tool_content", CONTENT_INPUT, content_received, entry_fn=start_content)
    funnel_tool_conv = _make("tool_funnel", FUNNEL_INPUT, funnel_received, entry_fn=start_funnel_tool)
    post_conv  = _make("tool_post", POST_INPUT, post_received, entry_fn=start_post)

    wf_customize_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_wf_customize, pattern=r"^wf_customize_\d+$")],
        states={WF_CUSTOMIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, wf_customize_received)]},
        fallbacks=[cancel_h],
        per_chat=True, per_user=True, per_message=False,
    )

    hook_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_hook_generator, pattern="^aitool_hooks$")],
        states={
            HOOK_NICHE:    [MessageHandler(filters.TEXT & ~filters.COMMAND, hook_niche_received)],
            HOOK_AUDIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, hook_audience_received)],
        },
        fallbacks=[cancel_h],
        per_chat=True, per_user=True, per_message=False,
    )

    cta_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_cta_generator, pattern="^aitool_ctas$")],
        states={
            CTA_PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, cta_platform_received)],
            CTA_GOAL:     [MessageHandler(filters.TEXT & ~filters.COMMAND, cta_goal_received)],
        },
        fallbacks=[cancel_h],
        per_chat=True, per_user=True, per_message=False,
    )

    videoidea_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_video_generator, pattern="^aitool_videos$")],
        states={VIDEO_NICHE_S: [MessageHandler(filters.TEXT & ~filters.COMMAND, video_niche_received)]},
        fallbacks=[cancel_h],
        per_chat=True, per_user=True, per_message=False,
    )

    funnelidea_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_funnel_generator, pattern="^aitool_funnel$")],
        states={FUNNEL_NICHE_S: [MessageHandler(filters.TEXT & ~filters.COMMAND, funnel_niche_received)]},
        fallbacks=[cancel_h],
        per_chat=True, per_user=True, per_message=False,
    )

    return [
        voice_conv, video_conv, auto_conv, content_conv, funnel_tool_conv, post_conv,
        wf_customize_conv,
        hook_conv, cta_conv, videoidea_conv, funnelidea_conv,
    ]
