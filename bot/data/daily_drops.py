import random
from datetime import date

DAILY_DROPS = [
    {
        "system_ru": "Система пакетного создания контента",
        "system_en": "Batch Content Creation System",
        "prompt_ru": "Промпт: «Дай 30 идей для видео в нише [НИША] для [АУДИТОРИЯ]. Конкретные, провокационные, без банальностей. Нумерованный список.»",
        "prompt_en": "Prompt: \"Give me 30 video ideas in [NICHE] for [AUDIENCE]. Specific, contrarian, no generic advice. Numbered list.\"",
        "action_ru": "Открой генератор контент-пака в боте → введи свою нишу → скопируй результат → запиши 3 видео сегодня.",
        "action_en": "Open the Content Pack generator in this bot → enter your niche → copy the output → record 3 videos today.",
    },
    {
        "system_ru": "Система авто-приветствия в Telegram",
        "system_en": "Telegram Auto-Welcome System",
        "prompt_ru": "Промпт: «Напиши 3 приветственных сообщения для нового подписчика Telegram канала о [НИША]. Сообщение 1: сразу. Сообщение 2: через 24ч. Сообщение 3: через 72ч. Без воды.»",
        "prompt_en": "Prompt: \"Write 3 welcome messages for a new Telegram subscriber of a [NICHE] channel. Message 1: instant. Message 2: 24h later. Message 3: 72h later. No filler.\"",
        "action_ru": "Настрой авто-ответчик в ManyBot или напиши 3 сообщения прямо сейчас. Подключи к боту.",
        "action_en": "Set up an auto-responder in ManyBot or write 3 messages right now. Connect to your bot.",
    },
    {
        "system_ru": "Хук-первая секунда",
        "system_en": "Hook-First System",
        "prompt_ru": "Промпт: «Перепиши этот хук как смелое утверждение с результатом в первых 5 словах: [ТВОЙ ХУКИ]»",
        "prompt_en": "Prompt: \"Rewrite this hook as a bold claim with the result in the first 5 words: [YOUR HOOK]\"",
        "action_ru": "Возьми своё последнее видео. Перепиши только первую строку. Перезалей или запиши новую версию сегодня.",
        "action_en": "Take your last video. Rewrite only the first line. Re-upload or record a new version today.",
    },
    {
        "system_ru": "Система репозиционирования контента",
        "system_en": "Content Repurposing System",
        "prompt_ru": "Промпт: «Адаптируй этот скрипт в 5 форматов: Telegram пост, Twitter тред, LinkedIn пост, YouTube описание, email. Скрипт: [СКРИПТ]»",
        "prompt_en": "Prompt: \"Adapt this script into 5 formats: Telegram post, Twitter thread, LinkedIn post, YouTube description, email. Script: [SCRIPT]\"",
        "action_ru": "Возьми своё лучшее видео этой недели → открой генератор поста Telegram в боте → скопируй → опубликуй прямо сейчас.",
        "action_en": "Take your best video this week → open the Telegram Post generator in this bot → copy → publish right now.",
    },
    {
        "system_ru": "Система конверсионного CTA",
        "system_en": "High-Converting CTA System",
        "prompt_ru": "Промпт: «Напиши 10 CTA для [ПЛАТФОРМА] с целью [ЦЕЛЬ]. Каждый под 20 слов. Конкретные цифры и результаты. Без банального 'подписывайся на больше'.»",
        "prompt_en": "Prompt: \"Write 10 CTAs for [PLATFORM] with goal [GOAL]. Each under 20 words. Specific numbers and results. No generic 'follow for more.'\"",
        "action_ru": "Открой генератор CTA в боте → введи платформу и цель → выбери лучший → добавь в следующее видео.",
        "action_en": "Open the CTA generator in this bot → enter platform and goal → pick the best one → add to your next video.",
    },
    {
        "system_ru": "Воронка за 30 минут",
        "system_en": "30-Minute Funnel System",
        "prompt_ru": "Промпт: «Создай минимальную воронку для [ПРОДУКТ/НИША]: источник трафика → точка входа → прогрев → конверсия. Только рабочие шаги.»",
        "prompt_en": "Prompt: \"Create a minimal funnel for [PRODUCT/NICHE]: traffic source → entry point → warm-up → conversion. Only working steps.\"",
        "action_ru": "Открой строитель воронок в боте → введи свою нишу → скопируй схему → настрой первый шаг сегодня.",
        "action_en": "Open the Funnel Builder in this bot → enter your niche → copy the map → set up the first step today.",
    },
    {
        "system_ru": "Система безликого контента",
        "system_en": "Faceless Content System",
        "prompt_ru": "Промпт: «Напиши войсовер скрипт (15–30 сек) о [ТЕМА] для [НИША]. Хук + 3 тезиса + CTA. Без приветствий. Готов к записи.»",
        "prompt_en": "Prompt: \"Write a voiceover script (15–30 sec) about [TOPIC] for [NICHE]. Hook + 3 points + CTA. No greetings. Ready to record.\"",
        "action_ru": "Открой войс-скрипт генератор → введи тему → вставь в ElevenLabs → смонтируй в CapCut → опубликуй.",
        "action_en": "Open the Voice Script generator → enter topic → paste into ElevenLabs → edit in CapCut → publish.",
    },
    {
        "system_ru": "Система удержания в Telegram",
        "system_en": "Telegram Retention System",
        "prompt_ru": "Промпт: «Напиши 7 постов для Telegram канала о [НИША] на неделю. Чередуй: ценность / вовлечение / шаблон / кейс. Без воды.»",
        "prompt_en": "Prompt: \"Write 7 Telegram channel posts about [NICHE] for one week. Alternate: value / engagement / template / case study. No filler.\"",
        "action_ru": "Открой генератор поста в боте → создай 3 поста прямо сейчас → запланируй на завтра.",
        "action_en": "Open the Post Generator in this bot → create 3 posts right now → schedule for tomorrow.",
    },
    {
        "system_ru": "n8n автоматизация за 20 минут",
        "system_en": "n8n Automation in 20 Minutes",
        "prompt_ru": "Промпт: «Опиши пошагово n8n воркфлоу для [ЦЕЛЬ]. Укажи каждый узел, триггер и действие. Только практические шаги.»",
        "prompt_en": "Prompt: \"Describe step by step an n8n workflow for [GOAL]. Name each node, trigger, and action. Practical steps only.\"",
        "action_ru": "Открой строитель автоматизации в боте → введи цель → скопируй систему → создай первый воркфлоу в n8n сегодня.",
        "action_en": "Open the Automation Builder in this bot → enter goal → copy the system → create your first n8n workflow today.",
    },
    {
        "system_ru": "Система роста через кросс-промо",
        "system_en": "Cross-Promo Growth System",
        "prompt_ru": "Промпт: «Напиши сообщение для владельца Telegram канала с предложением взаимного шаутаута. Коротко, конкретно, с ценностью для него.»",
        "prompt_en": "Prompt: \"Write a DM to a Telegram channel owner proposing a mutual shoutout. Short, specific, value-first.\"",
        "action_ru": "Найди 5 каналов в смежных нишах → напиши каждому сегодня → договорись хотя бы с одним на этой неделе.",
        "action_en": "Find 5 channels in adjacent niches → message each one today → close at least one deal this week.",
    },
]


def get_daily_drop():
    today = date.today()
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    return random.choice(DAILY_DROPS)
