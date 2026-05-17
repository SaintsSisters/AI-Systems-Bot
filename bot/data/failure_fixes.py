FAILURE_FIXES = [
    {
        "emoji": "❌",
        "title_ru": "Видео не зашло: слабый хук",
        "title_en": "Video Failed: Weak Hook",
        "content_ru": """❌ *ЧТО НЕ СРАБОТАЛО*
Видео с хуком "Привет, сегодня поговорим о..."
Результат: 72% вышли за 4 секунды. 200 просмотров.

🔧 *ЧТО МЕНЯТЬ В СИСТЕМЕ*
→ Никаких мягких открытий — только результат в первую строку
→ Тестируй 3 варианта хука перед записью
→ Используй генератор хуков в этом боте

✅ *ПРАВИЛО-ФИКС*
Первая строка = результат, который зритель получит.
Если первое слово — "Я", "Сегодня", "Привет" → перепиши.

📋 *ШАБЛОН ЗАМЕНЫ*
❌ "Привет! Сегодня расскажу про [ТЕМУ]"
✅ "Я [РЕЗУЛЬТАТ] за [СРОК]. Вот точная система."
✅ "[ЦИФРА] инструментов, которые заменили мне [СТАРЫЙ СПОСОБ]."
✅ "Все советуют [X]. Они неправы. Вот что реально работает." """,

        "content_en": """❌ *WHAT FAILED*
Video with hook "Hey everyone, today we're going to talk about..."
Result: 72% dropped off in 4 seconds. 200 views.

🔧 *WHAT TO CHANGE IN THE SYSTEM*
→ No soft openings — result first, always
→ Test 3 hook variants before recording
→ Use the hook generator in this bot

✅ *FIX RULE*
First line = the result the viewer will get.
If the first word is "I", "Today", "Hey" → rewrite it.

📋 *REPLACEMENT TEMPLATE*
❌ "Hey! Today I'll tell you about [TOPIC]"
✅ "I [RESULT] in [TIMEFRAME]. Here's the exact system."
✅ "[NUMBER] tools that replaced [OLD WAY] for me."
✅ "Everyone says [X]. They're wrong. Here's what actually works." """,
    },
    {
        "emoji": "📊",
        "title_ru": "Удержание падает на 3-й секунде",
        "title_en": "Retention Drops at 3 Seconds",
        "content_ru": """❌ *ЧТО НЕ СРАБОТАЛО*
Каждое видео с "мягким" открытием теряло 50%+ к 5-й секунде.

🔧 *ЧТО МЕНЯТЬ В СИСТЕМЕ*
→ Убрать любое вступление из скриптов
→ Добавить паттерн-интерапт на 2-й секунде (смена кадра, текст на экране, движение)
→ Проверять хук: есть ли причина смотреть дальше в первых 5 словах?

✅ *ПРАВИЛО-ФИКС*
Если первое предложение начинается с "Так что..." или "Знаешь..." → это провал.
Начинай с данных, результата или смелого утверждения.

📋 *ШАБЛОН ПАТТЕРН-ИНТЕРАПТ*
Секунда 0: [СМЕЛАЯ ФРАЗА]
Секунда 1: [СМЕНА КАДРА / СУБТИТР]
Секунда 2: [КОНКРЕТИКА — цифра или результат]
Секунда 3: [ОБЕЩАНИЕ — "вот как"]""",

        "content_en": """❌ *WHAT FAILED*
Every video with a "soft" opening lost 50%+ of viewers by second 5.

🔧 *WHAT TO CHANGE IN THE SYSTEM*
→ Remove all intros from scripts
→ Add a pattern interrupt at second 2 (cut, on-screen text, movement)
→ Check every hook: is there a reason to keep watching in the first 5 words?

✅ *FIX RULE*
If the first sentence starts with "So..." or "You know..." → that's a fail.
Start with data, a result, or a bold claim.

📋 *PATTERN INTERRUPT TEMPLATE*
Second 0: [BOLD STATEMENT]
Second 1: [CUT / SUBTITLE]
Second 2: [SPECIFICS — number or result]
Second 3: [PROMISE — "here's how"]""",
    },
    {
        "emoji": "📢",
        "title_ru": "Слабые CTA — ноль конверсий",
        "title_en": "Weak CTAs — Zero Conversions",
        "content_ru": """❌ *ЧТО НЕ СРАБОТАЛО*
CTA "Подписывайся на больше контента" конвертировал в 0.3 подписки на 1000 просмотров.

🔧 *ЧТО МЕНЯТЬ В СИСТЕМЕ*
→ Заменить все generic CTA на конкретные
→ Добавить соцдоказательство ("уже X человек")
→ Указать что конкретно получит подписчик

✅ *ПРАВИЛО-ФИКС*
CTA должен отвечать на вопрос "а мне-то что?"
Не что делать — а что получить.

📋 *ШАБЛОНЫ ЗАМЕНЫ*
❌ "Подписывайся на больше контента"
✅ "Подписывайся — каждое утро в 8:00 выхожу с [ЧТО]"
✅ "Уже [ЦИФРА]+ авторов используют эту систему — ссылка в био"
✅ "Полный [РЕСУРС] закреплён в моём Telegram — ссылка в профиле"
✅ "Сохрани — пригодится когда начнёшь [ДЕЙСТВИЕ]" """,

        "content_en": """❌ *WHAT FAILED*
CTA "Follow for more content" converted at 0.3 follows per 1,000 views.

🔧 *WHAT TO CHANGE IN THE SYSTEM*
→ Replace all generic CTAs with specific ones
→ Add social proof ("X people already")
→ Specify exactly what the follower gets

✅ *FIX RULE*
CTA must answer "what's in it for me?"
Not what to do — but what they get.

📋 *REPLACEMENT TEMPLATES*
❌ "Follow for more content"
✅ "Follow — I post [WHAT] every morning at 8am"
✅ "[NUMBER]+ creators already use this system — link in bio"
✅ "Full [RESOURCE] pinned in my Telegram — link in bio"
✅ "Save this — you'll need it when you start [ACTION]" """,
    },
    {
        "emoji": "🧠",
        "title_ru": "Ловушка перфекционизма",
        "title_en": "The Overthinking Trap",
        "content_ru": """❌ *ЧТО НЕ СРАБОТАЛО*
3 недели "планирования системы". 0 опубликованных видео.
Стратегический документ на 40 страниц. 0 результатов.

🔧 *ЧТО МЕНЯТЬ В СИСТЕМЕ*
→ Установить дедлайн: "Через 3 дня — первое видео"
→ Правило 80%: публикуй при 80% готовности
→ Сначала данные из реальных видео — потом улучшение системы

✅ *ПРАВИЛО-ФИКС*
Плохая система которая работает > идеальная система в заметках.
Первые 50 видео — все будут плохими. Публикуй их.

📋 *ПЛАН ЗАПУСКА (АНТИПЕРФЕКЦИОНИЗМ)*
День 1: Запиши видео (любое) — опубликуй
День 2: Запиши ещё одно — опубликуй
День 3: Посмотри на аналитику — оптимизируй хук
Неделя 2: Добавь один улучшенный элемент
Правило: улучшать только одно за раз""",

        "content_en": """❌ *WHAT FAILED*
3 weeks "planning the system." 0 videos published.
40-page strategy document. 0 results.

🔧 *WHAT TO CHANGE IN THE SYSTEM*
→ Set a deadline: "First video in 3 days"
→ The 80% rule: publish when 80% ready
→ Get real data from actual videos first — then optimize

✅ *FIX RULE*
A bad system that runs beats a perfect system in your notes.
Your first 50 videos will all be bad — publish them anyway.

📋 *LAUNCH PLAN (ANTI-PERFECTIONISM)*
Day 1: Record a video (any) — publish it
Day 2: Record another — publish it
Day 3: Check analytics — optimize the hook
Week 2: Add one improved element
Rule: improve only one thing at a time""",
    },
    {
        "emoji": "🏗️",
        "title_ru": "Не та платформа",
        "title_en": "Wrong Platform First",
        "content_ru": """❌ *ЧТО НЕ СРАБОТАЛО*
6 месяцев на YouTube в нише где аудитория сидит в TikTok.
Результат: 400 подписчиков и выгорание.

🔧 *ЧТО МЕНЯТЬ В СИСТЕМЕ*
→ Исследовать где аудитория до старта, не после
→ Смотреть на вовлечённость, а не на количество подписчиков в нише
→ Стартовать с одной платформой — не распыляться

✅ *ПРАВИЛО-ФИКС*
Дистрибуция — стратегическое решение.
Правильная платформа важнее качества контента на старте.

📋 *КАК ВЫБРАТЬ ПЛАТФОРМУ*
Шаг 1: Найди 10 лидеров в своей нише
Шаг 2: Где у них больше вовлечённость (не подписчики)?
Шаг 3: Где они сами активнее всего публикуют?
Шаг 4: Выбери эту платформу. Одну. Сначала.

Иерархия 2025: TikTok → Reels → Shorts → Telegram""",

        "content_en": """❌ *WHAT FAILED*
6 months on YouTube in a niche where the audience lives on TikTok.
Result: 400 subscribers and burnout.

🔧 *WHAT TO CHANGE IN THE SYSTEM*
→ Research where the audience is before starting, not after
→ Look at engagement, not subscriber counts, in your niche
→ Start with one platform — don't spread thin

✅ *FIX RULE*
Distribution is a strategic decision.
The right platform matters more than content quality at the start.

📋 *HOW TO CHOOSE A PLATFORM*
Step 1: Find 10 leaders in your niche
Step 2: Where do they have more engagement (not followers)?
Step 3: Where do they publish most actively?
Step 4: Choose that platform. One. First.

2025 hierarchy: TikTok → Reels → Shorts → Telegram""",
    },
    {
        "emoji": "🤖",
        "title_ru": "AI без стратегии",
        "title_en": "AI Without Strategy",
        "content_ru": """❌ *ЧТО НЕ СРАБОТАЛО*
Использование ChatGPT для генерации идей без стратегии.
Результат: 200 идей, 0 опубликованных видео.

🔧 *ЧТО МЕНЯТЬ В СИСТЕМЕ*
→ Перед запросом — написать одно предложение: "Какой результат мне нужен?"
→ Использовать готовые промпты (этот бот) вместо импровизации
→ AI — инструмент выполнения, не инструмент стратегии

✅ *ПРАВИЛО-ФИКС*
AI ускоряет движение в правильном направлении.
Если направление неверное — AI просто быстрее заведёт не туда.

📋 *ПРОТОКОЛ РАБОТЫ С AI*
1. Определи цель (1 предложение)
2. Выбери инструмент в этом боте (хуки / скрипт / воронка)
3. Введи нишу → получи результат
4. Используй сразу (не копи "на потом")
5. Публикуй → анализируй → повторяй""",

        "content_en": """❌ *WHAT FAILED*
Using ChatGPT to generate ideas without a strategy.
Result: 200 ideas, 0 published videos.

🔧 *WHAT TO CHANGE IN THE SYSTEM*
→ Before any prompt — write one sentence: "What result do I need?"
→ Use ready-made prompts (this bot) instead of improvising
→ AI is an execution tool, not a strategy tool

✅ *FIX RULE*
AI accelerates movement in the right direction.
If the direction is wrong — AI just gets you lost faster.

📋 *AI WORK PROTOCOL*
1. Define goal (1 sentence)
2. Choose a tool in this bot (hooks / script / funnel)
3. Enter niche → get output
4. Use it immediately (don't save "for later")
5. Publish → analyze → repeat""",
    },
]
