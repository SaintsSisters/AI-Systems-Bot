import json
import os
from typing import Any, Optional

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage")
STATE_FILE = os.path.join(STORAGE_DIR, "user_state.json")


def _load() -> dict:
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save(data: dict) -> None:
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_state(user_id: int) -> dict:
    data = _load()
    return data.get(str(user_id), {
        "active_tool": None,
        "awaiting_input": False,
        "step": 1,
        "data": {},
    })


def set_state(user_id: int, active_tool: Optional[str], awaiting_input: bool,
              step: int = 1, extra: Optional[dict] = None) -> None:
    data = _load()
    uid = str(user_id)
    data[uid] = {
        "active_tool": active_tool,
        "awaiting_input": awaiting_input,
        "step": step,
        "data": extra or {},
    }
    _save(data)


def reset_state(user_id: int) -> None:
    data = _load()
    uid = str(user_id)
    data[uid] = {
        "active_tool": None,
        "awaiting_input": False,
        "step": 1,
        "data": {},
    }
    _save(data)


def store_data(user_id: int, key: str, value: Any) -> None:
    data = _load()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"active_tool": None, "awaiting_input": False, "step": 1, "data": {}}
    data[uid].setdefault("data", {})[key] = value
    _save(data)


def advance_step(user_id: int) -> None:
    data = _load()
    uid = str(user_id)
    if uid in data:
        data[uid]["step"] = data[uid].get("step", 1) + 1
        _save(data)
