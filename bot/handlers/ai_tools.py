from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.constants import ParseMode

from bot.services.openai_service import (
    generate_hooks,
    generate_ctas,
    generate_video_ideas,
    generate_funnel_idea,
)
from bot.handlers.keyboards import ai_tools_keyboard, back_to_main
from bot.utils.storage import track_usage

HOOK_NICHE, HOOK_AUDIENCE = range(2)
CTA_PLATFORM, CTA_GOAL = range(10, 12)
VIDEO_NICHE = 20
FUNNEL_NICHE = 30

CANCEL_TEXT = "❌ Cancelled. Use /start to go back to the main menu."


async def start_hook_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🪝 *HOOK GENERATOR*\n\nStep 1 of 2\n\n*What's your niche?*\n_(e.g. AI automation, fitness, personal finance, productivity)_",
        parse_mode=ParseMode.MARKDOWN,
    )
    return HOOK_NICHE


async def hook_niche_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["hook_niche"] = update.message.text
    await update.message.reply_text(
        "🪝 *HOOK GENERATOR*\n\nStep 2 of 2\n\n*Who's your target audience?*\n_(e.g. beginner entrepreneurs, busy parents, freelance designers)_",
        parse_mode=ParseMode.MARKDOWN,
    )
    return HOOK_AUDIENCE


async def hook_audience_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    niche = context.user_data.get("hook_niche", "")
    audience = update.message.text
    track_usage(update.effective_user.id, "hook_generator")

    thinking = await update.message.reply_text("⚡ Generating 10 hooks...")

    try:
        result = await generate_hooks(niche, audience)
        await thinking.delete()
        await update.message.reply_text(
            f"🪝 *10 HOOKS FOR {niche.upper()}*\n\n{result}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_main(),
        )
    except Exception as e:
        await thinking.edit_text(f"Something went wrong. Please try again.")

    return ConversationHandler.END


async def start_cta_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📢 *CTA GENERATOR*\n\nStep 1 of 2\n\n*Which platform?*\n_(e.g. TikTok, Instagram, YouTube, Telegram, LinkedIn)_",
        parse_mode=ParseMode.MARKDOWN,
    )
    return CTA_PLATFORM


async def cta_platform_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["cta_platform"] = update.message.text
    await update.message.reply_text(
        "📢 *CTA GENERATOR*\n\nStep 2 of 2\n\n*What's your goal?*\n_(e.g. grow followers, drive Telegram joins, sell a product, get email subscribers)_",
        parse_mode=ParseMode.MARKDOWN,
    )
    return CTA_GOAL


async def cta_goal_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    platform = context.user_data.get("cta_platform", "")
    goal = update.message.text
    track_usage(update.effective_user.id, "cta_generator")

    thinking = await update.message.reply_text("⚡ Generating 10 CTAs...")

    try:
        result = await generate_ctas(platform, goal)
        await thinking.delete()
        await update.message.reply_text(
            f"📢 *10 CTAs FOR {platform.upper()}*\n\n{result}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_main(),
        )
    except Exception:
        await thinking.edit_text("Something went wrong. Please try again.")

    return ConversationHandler.END


async def start_video_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🎬 *VIDEO IDEA GENERATOR*\n\n*What's your niche?*\n_(e.g. AI tools, crypto, cooking, self-improvement, SaaS)_",
        parse_mode=ParseMode.MARKDOWN,
    )
    return VIDEO_NICHE


async def video_niche_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    niche = update.message.text
    track_usage(update.effective_user.id, "video_generator")

    thinking = await update.message.reply_text("⚡ Generating 10 video ideas...")

    try:
        result = await generate_video_ideas(niche)
        await thinking.delete()
        await update.message.reply_text(
            f"🎬 *10 VIDEO IDEAS FOR {niche.upper()}*\n\n{result}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_main(),
        )
    except Exception:
        await thinking.edit_text("Something went wrong. Please try again.")

    return ConversationHandler.END


async def start_funnel_generator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔁 *FUNNEL IDEA GENERATOR*\n\n*What's your product or niche?*\n_(e.g. AI automation course, freelance design services, Telegram growth consulting)_",
        parse_mode=ParseMode.MARKDOWN,
    )
    return FUNNEL_NICHE


async def funnel_niche_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    product_niche = update.message.text
    track_usage(update.effective_user.id, "funnel_generator")

    thinking = await update.message.reply_text("⚡ Building your funnel idea...")

    try:
        result = await generate_funnel_idea(product_niche)
        await thinking.delete()
        await update.message.reply_text(
            f"🔁 *FUNNEL IDEA*\n\n{result}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_main(),
        )
    except Exception:
        await thinking.edit_text("Something went wrong. Please try again.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(CANCEL_TEXT, reply_markup=back_to_main())
    return ConversationHandler.END


def get_ai_tool_conversations():
    cancel_handler = CommandHandler("cancel", cancel)

    hook_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_hook_generator, pattern="^aitool_hooks$")],
        states={
            HOOK_NICHE: [MessageHandler(filters.TEXT & ~filters.COMMAND, hook_niche_received)],
            HOOK_AUDIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, hook_audience_received)],
        },
        fallbacks=[cancel_handler],
        per_chat=True,
        per_user=True,
        per_message=False,
    )

    cta_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_cta_generator, pattern="^aitool_ctas$")],
        states={
            CTA_PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, cta_platform_received)],
            CTA_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, cta_goal_received)],
        },
        fallbacks=[cancel_handler],
        per_chat=True,
        per_user=True,
        per_message=False,
    )

    video_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_video_generator, pattern="^aitool_videos$")],
        states={
            VIDEO_NICHE: [MessageHandler(filters.TEXT & ~filters.COMMAND, video_niche_received)],
        },
        fallbacks=[cancel_handler],
        per_chat=True,
        per_user=True,
        per_message=False,
    )

    funnel_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_funnel_generator, pattern="^aitool_funnel$")],
        states={
            FUNNEL_NICHE: [MessageHandler(filters.TEXT & ~filters.COMMAND, funnel_niche_received)],
        },
        fallbacks=[cancel_handler],
        per_chat=True,
        per_user=True,
        per_message=False,
    )

    return [hook_conv, cta_conv, video_conv, funnel_conv]
