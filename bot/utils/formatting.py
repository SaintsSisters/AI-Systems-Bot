def bold(text: str) -> str:
    return f"*{text}*"


def code(text: str) -> str:
    return f"`{text}`"


def section(title: str, emoji: str = "") -> str:
    prefix = f"{emoji} " if emoji else ""
    return f"{prefix}*{title.upper()}*"


def divider() -> str:
    return "─" * 28


def workflow_card(workflow: dict) -> str:
    steps = "\n".join(f"  {i+1}. {step}" for i, step in enumerate(workflow["steps"]))
    tools = " · ".join(workflow["tools"])
    return f"""{workflow['emoji']} *{workflow['title']}*

{workflow['explanation']}

*Steps:*
{steps}

*Recommended tools:* {tools}
*Traffic source:* {workflow['traffic_source']}
*Monetization:* {workflow['monetization']}"""


def tool_card(tool: dict) -> str:
    return f"""{tool['emoji']} *{tool['name']}*

📌 *What it does:* {tool['what']}
💡 *Why it matters:* {tool['why']}
🔧 *How creators use it:* {tool['how']}"""


def template_card(template: dict) -> str:
    lines = [f"📋 *{template['name']}*", "", f"`{template['template']}`"]
    if "example" in template:
        lines += ["", f"*Example:*", f"_{template['example']}_"]
    return "\n".join(lines)


def experiment_card(exp: dict) -> str:
    return f"""{exp['emoji']} *{exp['title']}*

🔬 *Hypothesis:* {exp['hypothesis']}
📋 *What was tested:* {exp['what_tested']}
📊 *Result:* {exp['result']}
✅ *Conclusion:* {exp['conclusion']}"""


def lesson_card(lesson: dict) -> str:
    return f"""{lesson['emoji']} *{lesson['title']}*

{lesson['content']}"""


def daily_drop_card(drop: dict) -> str:
    return f"""{drop['content']}

{divider()}
_Come back tomorrow for another drop._"""


def premium_card() -> str:
    return """👑 *AI SYSTEMS HUB — PREMIUM*

Premium unlocks the full operating system:

🔐 *Advanced Workflows*
→ Complete SaaS build workflows
→ Monetization system blueprints
→ Subscriber acquisition funnels

📦 *Private Automation Packs*
→ n8n workflow templates (ready to import)
→ Zapier zap collections
→ AI prompt libraries

🎯 *Advanced Templates*
→ High-converting funnel sequences
→ Email automation scripts
→ Telegram channel launch playbooks

📊 *Exclusive Experiments*
→ Full case studies with data
→ Revenue breakdowns
→ Behind-the-scenes build logs

🤝 *Private Community Access*
→ Weekly live sessions
→ Direct feedback on your systems
→ Member collaboration

─────────────────────────────
*Launching soon. Early access pricing locked for waitlist members.*"""


def channel_card(channel_url: str = "https://t.me/aisystemshub") -> str:
    return f"""📡 *AI SYSTEMS HUB — CHANNEL*

The official channel behind this bot.

*What we publish:*
→ Daily workflow breakdowns
→ AI tool reviews and comparisons
→ Real experiment results
→ Automation system templates
→ Growth case studies

*Who it's for:*
Creators, marketers, Telegram builders, and automation enthusiasts who want practical systems — not motivation.

*Latest:* New funnel teardown dropped this week.

─────────────────────────────
Join to stay in the loop 👇"""
