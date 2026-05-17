import random
from datetime import date

DAILY_DROPS = [
    {
        "type": "workflow",
        "title": "The 30-Minute Content Batch",
        "content": """⚡ *WORKFLOW DROP*

*The 30-Minute Content Batch*

Most creators waste 3 hours per video. Here's how to produce 7 pieces of content in 30 minutes:

→ 10 min: Script 3 short-form videos with ChatGPT
→ 5 min: Record all 3 in one session (no stops)
→ 10 min: Edit using a single CapCut template
→ 5 min: Write captions and schedule across platforms

*Total:* 30 minutes → 7 content pieces (3 videos + 4 platform reposts)

The goal is volume without sacrificing the hook. Scripts and templates are your leverage.""",
    },
    {
        "type": "automation",
        "title": "Auto-Welcome Sequence",
        "content": """🤖 *AUTOMATION TRICK*

*Build a Telegram Auto-Welcome That Actually Converts*

Most welcome messages are generic. This one works:

→ Message 1 (instant): Welcome + who this channel is for + what to expect
→ Message 2 (24h later): Your best post or free resource
→ Message 3 (72h later): Community invite or premium teaser

*Tools:* ManyBot (no-code) or python-telegram-bot (custom)

A strong welcome sequence increases 30-day retention by 40-60%. Most channels skip it entirely — that's your edge.""",
    },
    {
        "type": "ai_tool",
        "title": "ChatGPT Prompt for 30 Content Ideas",
        "content": """🧠 *AI TOOL DROP*

*The Prompt That Generates 30 Content Ideas in 60 Seconds*

Use this exact prompt:

`"I create content about [NICHE] for [AUDIENCE]. Give me 30 short-form video ideas that are specific, contrarian, or counter-intuitive. Format as a numbered list. No generic advice. Focus on tactics and systems."`

*Why it works:*
→ "Contrarian or counter-intuitive" forces specificity
→ "No generic advice" filters out filler
→ "Tactics and systems" matches what high-performers engage with

Run this once per week. You'll never run out of ideas.""",
    },
    {
        "type": "growth",
        "title": "The Cross-Promo System",
        "content": """📡 *GROWTH TIP*

*The Cross-Promo System That Doesn't Feel Spammy*

Most cross-promo attempts fail because they're transactional. Here's what works:

→ Find 3 channels in adjacent niches (not direct competitors)
→ Engage with their content for 2 weeks first (genuine reactions, shares)
→ Reach out with specific value: "I'll promote your channel to my X members if you do the same"
→ Create a dedicated post about their channel — not a generic shoutout

*Key:* The more specific and genuine the post, the better it converts.
Lazy shoutouts get ignored. Genuine endorsements build communities.""",
    },
    {
        "type": "content",
        "title": "The Repurposing Stack",
        "content": """♻️ *CONTENT SYSTEM*

*Turn 1 Video Into 8 Pieces of Content*

One 60-second video → 8 outputs:

1. Original TikTok
2. Instagram Reel (same or slightly cropped)
3. YouTube Short
4. Twitter/X video clip
5. LinkedIn post (text version of the script)
6. Telegram value drop (bullet point version)
7. Email newsletter section
8. Thread on X (expanded point by point)

*Tools:* Repurpose.io for automation, Canva for text graphics

Stop creating from scratch every day. Multiply what you already made.""",
    },
    {
        "type": "funnel",
        "title": "The One-Asset Funnel",
        "content": """🔁 *FUNNEL SYSTEM*

*The Simplest Funnel That Still Works*

You don't need a website. You don't need a course. You need:

1. One piece of short-form content with a strong CTA
2. One Telegram channel or email list
3. One free resource worth having (checklist, template, swipe file)
4. One paid offer (even if it's just consulting)

*The flow:*
TikTok/Reel → Bio Link → Telegram Join → Free Resource → Paid Offer

This converts because every step delivers value before asking for anything.
Most people skip steps 3 and 4. Don't be most people.""",
    },
    {
        "type": "mindset",
        "title": "Ship the Ugly Version",
        "content": """🚀 *SYSTEMS INSIGHT*

*Ship the Ugly Version*

The creator who posts an 80% video today beats the one waiting for 100% next month.

*The math:*
→ Creator A: 1 perfect video per month = 12 videos/year
→ Creator B: 1 decent video per day = 365 videos/year

After year 1, Creator B has 30x more data, 30x more reps, and 30x more chances to go viral.

Perfection is a waiting room for irrelevance.
*Ship it. Learn. Improve. Repeat.*""",
    },
    {
        "type": "automation",
        "title": "n8n Telegram Notification Bot",
        "content": """⚙️ *AUTOMATION TRICK*

*Build a Notification Bot in n8n in 20 Minutes*

This workflow sends you a Telegram message every time:
→ Someone subscribes to your email list
→ A new sale comes in
→ A form is submitted on your site

*Setup:*
1. Create a free n8n account (or self-host)
2. Use the Telegram node with your bot token
3. Connect your trigger (Typeform, ConvertKit, Gumroad, etc.)
4. Set the message template with the key data fields
5. Activate

*Result:* Real-time awareness of your business without checking dashboards all day.""",
    },
    {
        "type": "growth",
        "title": "The First 1000 Members Playbook",
        "content": """📈 *GROWTH SYSTEM*

*How to Get Your First 1,000 Telegram Members*

Week 1-2: Foundation
→ Set up channel with clear niche, strong description, pinned value post
→ Post 2x/day minimum

Week 3-4: Cross-promo
→ Find 10 Telegram groups in adjacent niches
→ Share value (not spam) in each group daily

Week 5-6: Content loop
→ Create 1 piece of short-form content/day with Telegram CTA
→ Use a free resource as the hook

Week 7-8: Network
→ DM 5 channel owners per week for shoutout swaps
→ Focus on channels 2-5x your size

Most people quit in week 3. The channel starts compounding in week 6.""",
    },
    {
        "type": "ai_tool",
        "title": "ElevenLabs for Faceless Content",
        "content": """🎙️ *AI TOOL DROP*

*ElevenLabs: The Faceless Content Creator's Secret*

ElevenLabs lets you generate human-quality voiceover from any text.

*Workflow:*
1. Write script with ChatGPT (2 min)
2. Paste into ElevenLabs, choose a voice (1 min)
3. Download audio → import into CapCut (1 min)
4. Add B-roll from Pexels over the audio
5. Add auto-captions in CapCut

*Total:* 15 minutes per video. No face. No mic. No setup.

*Best voices:* Rachel (calm), Josh (authoritative), Bella (friendly)
Free tier: 10,000 characters/month — enough for 20+ videos.""",
    },
]


def get_daily_drop():
    today = date.today()
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    drop = random.choice(DAILY_DROPS)
    return drop
