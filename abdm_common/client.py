"""HTTP helpers for ABDM APIs."""

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import config

from abdm_common.settings import current_env, resolve_url
from abdm_common.tokens import request_id, utc_timestamp

_DEFAULT_TIMEOUT = 60


def _needs_cm_id(url: str) -> bool:
    return "dev.abdm.gov.in" in url or "/api/hiecm/" in url or "/gateway/" in url


def _base_headers(
    extra: dict[str, str] | None,
    gateway_token: str | None,
    x_token: str | None,
    url: str,
) -> dict[str, str]:
    h: dict[str, str] = {
        "REQUEST-ID": request_id(),
        "TIMESTAMP": utc_timestamp(),
    }
    if extra:
        h.update(extra)
    if gateway_token:
        h["Authorization"] = f"Bearer {gateway_token}"
    if x_token:
        h["X-Token"] = f"Bearer {x_token}"
    if _needs_cm_id(url) and getattr(config, "X_CM_ID", None) and "X-CM-ID" not in h:
        h["X-CM-ID"] = config.X_CM_ID
    return h


def _json_response(req: Request) -> dict[str, Any]:
    try:
        with urlopen(req, timeout=_DEFAULT_TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except HTTPError as err:
        error_body = err.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {err.code} for {req.full_url}\nResponse: {error_body}"
        ) from err
    except URLError as err:
        raise RuntimeError(f"Network error for {req.full_url}: {err}") from err


def post_json(
    url: str,
    payload: dict[str, Any],
    *,
    gateway_token: str | None = None,
    x_token: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    url = resolve_url(url, current_env())
    headers = _base_headers(
        {**(extra_headers or {}), "Content-Type": "application/json"},
        gateway_token,
        x_token,
        url,
    )
    req = Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    return _json_response(req)


def patch_json(
    url: str,
    payload: dict[str, Any],
    *,
    gateway_token: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    url = resolve_url(url, current_env())
    headers = _base_headers(
        {**(extra_headers or {}), "Content-Type": "application/json"},
        gateway_token,
        None,
        url,
    )
    req = Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="PATCH",
    )
    return _json_response(req)


def put_json(
    url: str,
    payload: dict[str, Any],
    *,
    gateway_token: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    url = resolve_url(url, current_env())
    headers = _base_headers(
        {**(extra_headers or {}), "Content-Type": "application/json"},
        gateway_token,
        None,
        url,
    )
    req = Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="PUT",
    )
    return _json_response(req)


def get_json(
    url: str,
    *,
    gateway_token: str | None = None,
    x_token: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    url = resolve_url(url, current_env())
    headers = _base_headers(extra_headers or {}, gateway_token, x_token, url)
    req = Request(url=url, headers=headers, method="GET")
    return _json_response(req)


def get_binary(
    url: str,
    *,
    gateway_token: str | None = None,
    x_token: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> tuple[bytes, str]:
    url = resolve_url(url, current_env())
    headers = _base_headers(extra_headers or {}, gateway_token, x_token, url)
    req = Request(url=url, headers=headers, method="GET")
    try:
        with urlopen(req, timeout=_DEFAULT_TIMEOUT) as resp:
            return resp.read(), resp.headers.get("Content-Type", "")
    except HTTPError as err:
        error_body = err.read()
        raise RuntimeError(
            f"HTTP {err.code} for {url}\nResponse: {error_body[:500]!r}"
        ) from err
    except URLError as err:
        raise RuntimeError(f"Network error for {url}: {err}") from err
