"""Shared helpers for ABDM CLI scripts."""

from abdm_common.client import get_binary, get_json, patch_json, post_json, put_json
from abdm_common.crypto import encrypt_with_public_key
from abdm_common.enrollment import download_abha_card, enroll_by_aadhaar, request_enrollment_otp
from abdm_common.session import (
    fetch_gateway_token,
    fetch_gateway_token_v05,
    fetch_public_certificate,
)
from abdm_common.settings import current_env, get_public_key_b64, resolve_url
from abdm_common.state import clear_state, load_state, save_state
from abdm_common.tokens import extract_x_token, request_id, utc_timestamp

__all__ = [
    "clear_state",
    "current_env",
    "download_abha_card",
    "encrypt_with_public_key",
    "enroll_by_aadhaar",
    "extract_x_token",
    "fetch_gateway_token",
    "fetch_gateway_token_v05",
    "fetch_public_certificate",
    "get_binary",
    "get_json",
    "get_public_key_b64",
    "load_state",
    "patch_json",
    "post_json",
    "put_json",
    "request_enrollment_otp",
    "request_id",
    "resolve_url",
    "save_state",
    "utc_timestamp",
]
