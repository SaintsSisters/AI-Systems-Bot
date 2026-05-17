import os
from openai import AsyncOpenAI
from bot.prompts.ai_tools import (
    HOOK_GENERATOR_PROMPT,
    CTA_GENERATOR_PROMPT,
    VIDEO_IDEA_GENERATOR_PROMPT,
    FUNNEL_IDEA_GENERATOR_PROMPT,
)

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

MODEL = "gpt-4o-mini"


async def _chat(prompt: str, max_tokens: int = 800) -> str:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()


async def generate_hooks(niche: str, audience: str) -> str:
    prompt = HOOK_GENERATOR_PROMPT.format(niche=niche, audience=audience)
    return await _chat(prompt)


async def generate_ctas(platform: str, goal: str) -> str:
    prompt = CTA_GENERATOR_PROMPT.format(platform=platform, goal=goal)
    return await _chat(prompt)


async def generate_video_ideas(niche: str) -> str:
    prompt = VIDEO_IDEA_GENERATOR_PROMPT.format(niche=niche)
    return await _chat(prompt)


async def generate_funnel_idea(product_niche: str) -> str:
    prompt = FUNNEL_IDEA_GENERATOR_PROMPT.format(product_niche=product_niche)
    return await _chat(prompt, max_tokens=400)
