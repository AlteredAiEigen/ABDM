"""Timestamps, request IDs, and token extraction from API JSON."""

import uuid
from datetime import datetime, timezone
from typing import Any


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def request_id() -> str:
    return str(uuid.uuid4())


def extract_x_token(data: dict[str, Any]) -> str | None:
    if not data:
        return None
    t = data.get("token")
    if t:
        return str(t)
    tokens = data.get("tokens")
    if isinstance(tokens, dict) and tokens.get("token"):
        return str(tokens["token"])
    return None
