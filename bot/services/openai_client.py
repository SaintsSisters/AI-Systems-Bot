"""
Single shared OpenAI client for the entire bot.
Both openai_service.py and action_service.py import from here.
"""
import os
import logging

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

_api_key = os.environ.get("OPENAI_API_KEY", "")
if not _api_key:
    logger.critical("OPENAI_API_KEY is missing from environment — AI tools will not work.")
else:
    logger.info("OpenAI client initialised (key present, length=%d).", len(_api_key))

client = AsyncOpenAI(api_key=_api_key)
MODEL = "gpt-4o-mini"


async def chat(prompt: str, max_tokens: int = 900) -> str:
    """Send a prompt and return the completion text. Raises on failure — caller must handle."""
    logger.info("OpenAI request sent (max_tokens=%d, prompt_len=%d).", max_tokens, len(prompt))
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.85,
    )
    text = response.choices[0].message.content.strip()
    logger.info("OpenAI response received (response_len=%d).", len(text))
    return text
