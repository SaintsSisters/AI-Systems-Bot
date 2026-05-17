from bot.services.openai_client import chat
from bot.prompts.ai_tools import (
    HOOK_GENERATOR_PROMPT,
    CTA_GENERATOR_PROMPT,
    VIDEO_IDEA_GENERATOR_PROMPT,
    FUNNEL_IDEA_GENERATOR_PROMPT,
)


async def generate_hooks(niche: str, audience: str) -> str:
    prompt = HOOK_GENERATOR_PROMPT.format(niche=niche, audience=audience)
    return await chat(prompt)


async def generate_ctas(platform: str, goal: str) -> str:
    prompt = CTA_GENERATOR_PROMPT.format(platform=platform, goal=goal)
    return await chat(prompt)


async def generate_video_ideas(niche: str) -> str:
    prompt = VIDEO_IDEA_GENERATOR_PROMPT.format(niche=niche)
    return await chat(prompt)


async def generate_funnel_idea(product_niche: str) -> str:
    prompt = FUNNEL_IDEA_GENERATOR_PROMPT.format(product_niche=product_niche)
    return await chat(prompt, max_tokens=500)
