import json
import os
from datetime import date
from typing import Optional

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage")
SUBSCRIBERS_FILE = os.path.join(STORAGE_DIR, "subscribers.json")


def _load() -> dict:
    if not os.path.exists(SUBSCRIBERS_FILE):
        return {}
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save(data: dict) -> None:
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def subscribe(user_id: int) -> None:
    data = _load()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"subscribed": True, "last_sent_date": None}
    else:
        data[uid]["subscribed"] = True
    _save(data)


def unsubscribe(user_id: int) -> None:
    data = _load()
    uid = str(user_id)
    if uid in data:
        data[uid]["subscribed"] = False
        _save(data)


def is_subscribed(user_id: int) -> bool:
    data = _load()
    uid = str(user_id)
    return data.get(uid, {}).get("subscribed", False)


def mark_sent(user_id: int) -> None:
    data = _load()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"subscribed": True, "last_sent_date": None}
    data[uid]["last_sent_date"] = date.today().isoformat()
    _save(data)


def already_sent_today(user_id: int) -> bool:
    data = _load()
    uid = str(user_id)
    last_sent = data.get(uid, {}).get("last_sent_date")
    return last_sent == date.today().isoformat()


def get_active_subscribers() -> list[int]:
    data = _load()
    return [
        int(uid)
        for uid, info in data.items()
        if info.get("subscribed", False)
    ]
