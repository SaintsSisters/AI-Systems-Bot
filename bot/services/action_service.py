import os
from openai import AsyncOpenAI
from bot.prompts.action_tools import (
    VOICE_SCRIPT_PROMPT,
    VIDEO_SCRIPT_PROMPT,
    AUTOMATION_BUILDER_PROMPT,
    CONTENT_PACK_PROMPT,
    FUNNEL_BUILDER_PROMPT,
    POST_GENERATOR_PROMPT,
    WORKFLOW_CUSTOMIZE_PROMPT,
)
from bot.utils.lang import lang_instruction

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"


async def _chat(prompt: str, max_tokens: int = 900) -> str:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.85,
    )
    return response.choices[0].message.content.strip()


async def gen_voice_script(topic: str, lang: str) -> str:
    prompt = VOICE_SCRIPT_PROMPT.format(lang_instruction=lang_instruction(lang), topic=topic)
    return await _chat(prompt)


async def gen_video_script(niche: str, lang: str) -> str:
    prompt = VIDEO_SCRIPT_PROMPT.format(lang_instruction=lang_instruction(lang), niche=niche)
    return await _chat(prompt)


async def gen_automation(goal: str, lang: str) -> str:
    prompt = AUTOMATION_BUILDER_PROMPT.format(lang_instruction=lang_instruction(lang), goal=goal)
    return await _chat(prompt)


async def gen_content_pack(niche: str, lang: str) -> str:
    prompt = CONTENT_PACK_PROMPT.format(lang_instruction=lang_instruction(lang), niche=niche)
    return await _chat(prompt, max_tokens=1200)


async def gen_funnel(product_niche: str, lang: str) -> str:
    prompt = FUNNEL_BUILDER_PROMPT.format(lang_instruction=lang_instruction(lang), product_niche=product_niche)
    return await _chat(prompt)


async def gen_telegram_post(topic: str, lang: str) -> str:
    prompt = POST_GENERATOR_PROMPT.format(lang_instruction=lang_instruction(lang), topic=topic)
    return await _chat(prompt)


async def gen_workflow_customized(workflow_name: str, user_input: str, lang: str) -> str:
    prompt = WORKFLOW_CUSTOMIZE_PROMPT.format(
        lang_instruction=lang_instruction(lang),
        workflow_name=workflow_name,
        user_input=user_input,
    )
    return await _chat(prompt)
