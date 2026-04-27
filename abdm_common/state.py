"""Optional JSON state file for multi-step CLI flows."""

import json
import os
from pathlib import Path
from typing import Any

import config


def _state_path() -> Path:
    custom = getattr(config, "STATE_FILE", "") or os.environ.get("ABDM_STATE_FILE", "")
    if custom:
        return Path(custom).expanduser()
    return Path.home() / ".abdm_session.json"


def load_state() -> dict[str, Any]:
    p = _state_path()
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(data: dict[str, Any]) -> None:
    p = _state_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass


def clear_state() -> None:
    p = _state_path()
    if p.is_file():
        p.unlink()
