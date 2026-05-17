import json
import os

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage")
USERS_FILE = os.path.join(STORAGE_DIR, "users.json")

DEFAULT_LANG = "ru"


def _load() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save(data: dict) -> None:
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_lang(user_id: int) -> str:
    data = _load()
    return data.get(str(user_id), {}).get("language", DEFAULT_LANG)


def set_lang(user_id: int, lang: str) -> None:
    data = _load()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {}
    data[uid]["language"] = lang
    _save(data)


def toggle_lang(user_id: int) -> str:
    current = get_lang(user_id)
    new_lang = "en" if current == "ru" else "ru"
    set_lang(user_id, new_lang)
    return new_lang


def lang_instruction(lang: str) -> str:
    if lang == "ru":
        return "Отвечай строго на русском языке. Не используй английский."
    return "Respond strictly in English."
