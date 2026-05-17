import json
import os
from datetime import datetime

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage")
USAGE_FILE = os.path.join(STORAGE_DIR, "usage.json")


def _load_usage() -> dict:
    if not os.path.exists(USAGE_FILE):
        return {}
    try:
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_usage(data: dict) -> None:
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def track_usage(user_id: int, action: str) -> None:
    data = _load_usage()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"actions": {}, "total": 0, "first_seen": datetime.now().isoformat()}
    if action not in data[uid]["actions"]:
        data[uid]["actions"][action] = 0
    data[uid]["actions"][action] += 1
    data[uid]["total"] += 1
    data[uid]["last_seen"] = datetime.now().isoformat()
    _save_usage(data)


def get_user_stats(user_id: int) -> dict:
    data = _load_usage()
    return data.get(str(user_id), {"total": 0, "actions": {}})


def get_global_stats() -> dict:
    data = _load_usage()
    total_users = len(data)
    total_actions = sum(u.get("total", 0) for u in data.values())
    return {"users": total_users, "actions": total_actions}
