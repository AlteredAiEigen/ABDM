"""Config, environment, and URL resolution."""

import os
from urllib.parse import urlparse, urlunparse

import config

ENV_HOSTS = {
    "sandbox": {
        "abha": "abhasbx.abdm.gov.in",
        "gateway": "dev.abdm.gov.in",
    },
    "prod": {
        "abha": "abdm.gov.in",
        "gateway": "abdm.gov.in",
    },
}


def current_env() -> str:
    e = getattr(config, "ABDM_ENV", "sandbox")
    return e if e in ENV_HOSTS else "sandbox"


def resolve_url(url: str, env: str | None = None) -> str:
    """Rewrite collection URLs for selected environment."""
    if not url:
        return url
    env = env or current_env()
    if env not in ENV_HOSTS:
        env = "sandbox"
    hosts = ENV_HOSTS[env]
    parsed = urlparse(url)
    if not parsed.netloc:
        return url
    host = parsed.netloc
    if "abhasbx.abdm.gov.in" in host or host.endswith("abdm.gov.in"):
        new_host = hosts["abha"]
    elif "dev.abdm.gov.in" in host:
        new_host = hosts["gateway"]
    else:
        return url
    return urlunparse(parsed._replace(netloc=new_host))


def get_public_key_b64() -> str:
    """Public key for RSA-OAEP; from config or env."""
    return config.PUBLIC_KEY_BASE64
