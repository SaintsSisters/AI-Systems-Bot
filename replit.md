# AI Systems Hub Bot

A production-ready Telegram bot that acts as a digital operating system for creators, marketers, and automation enthusiasts — covering AI workflows, content pipelines, Telegram growth, traffic funnels, and practical experiments.

## Run & Operate

- `python main.py` — run the Telegram bot (via the "AI Systems Hub Bot" workflow)
- Required secrets: `TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY`

## Stack

- Python 3 + python-telegram-bot 21.x
- OpenAI API (gpt-4o-mini) for AI tool generation
- Local JSON storage (`bot/storage/usage.json`) for lightweight usage tracking
- No database required

## Where things live

- `main.py` — entry point, wires up all handlers
- `bot/handlers/menu.py` — all main menu and section navigation callbacks
- `bot/handlers/ai_tools.py` — ConversationHandlers for 4 AI tools
- `bot/handlers/keyboards.py` — all InlineKeyboardMarkup builders
- `bot/data/` — static content: workflows, toolbox, templates, experiments, lessons, daily drops
- `bot/prompts/ai_tools.py` — OpenAI prompt templates
- `bot/services/openai_service.py` — OpenAI API calls
- `bot/utils/formatting.py` — message card formatters
- `bot/utils/storage.py` — lightweight JSON usage tracking
- `bot/storage/usage.json` — auto-created on first use

## Architecture decisions

- All menus use InlineKeyboardMarkup for fast, stateless navigation
- AI tools use ConversationHandlers for multi-step input flows
- Daily drops are deterministically seeded by date — same drop all day, rotates daily
- Usage tracking is fire-and-forget JSON (no DB) — acceptable for MVP scale
- OpenAI calls use gpt-4o-mini for speed and cost efficiency

## Product

Nine sections accessible from the main menu:
1. **Workflows** — 6 ready-to-use digital system blueprints with steps, tools, traffic source, monetization
2. **Toolbox** — 7 categories of curated AI/automation tools with paginated navigation
3. **Templates** — Hook, CTA, post structure, funnel, and viral opening templates
4. **Experiments** — Real growth/content experiments with hypothesis, result, and conclusion
5. **AI Tools** — 4 AI generators: hooks, CTAs, video ideas, funnel ideas (powered by OpenAI)
6. **Daily Drop** — Date-seeded rotating daily content drop with 10 types in the pool
7. **Lessons** — Honest failure breakdowns and practical insights
8. **Premium** — Placeholder upgrade flow with waitlist capture
9. **Channel** — Channel description with join button

## User preferences

- Modular architecture — each section in its own file
- No database for MVP — JSON storage only
- Clean UX — inline keyboards, back buttons, no long paragraphs

## Gotchas

- Bot token must be set in Replit Secrets as `TELEGRAM_BOT_TOKEN`
- OpenAI key must be set as `OPENAI_API_KEY`
- Restart the workflow after any code change: "AI Systems Hub Bot"
- `bot/storage/` directory is auto-created on first usage event
