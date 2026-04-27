"""Gateway session and public certificate."""

import config

from abdm_common.client import get_json, post_json


def fetch_gateway_token() -> str:
    data = post_json(
        config.SESSION_URL,
        {
            "clientId": config.CLIENT_ID,
            "clientSecret": config.CLIENT_SECRET,
            "grantType": config.GRANT_TYPE,
        },
    )
    token = data.get("accessToken")
    if not token:
        raise RuntimeError(f"Session response did not include accessToken: {data}")
    return str(token)


def fetch_gateway_token_v05() -> str:
    """DL flow may use v0.5 sessions endpoint."""
    data = post_json(
        config.SESSION_URL_V05,
        {
            "clientId": config.CLIENT_ID,
            "clientSecret": config.CLIENT_SECRET,
            "grantType": config.GRANT_TYPE,
        },
    )
    token = data.get("accessToken")
    if not token:
        raise RuntimeError(f"v0.5 session did not include accessToken: {data}")
    return str(token)


def fetch_public_certificate(gateway_token: str | None = None) -> dict:
    return get_json(
        config.PUBLIC_CERTIFICATE_URL,
        gateway_token=gateway_token,
    )
