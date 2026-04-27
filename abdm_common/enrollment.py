"""Enrollment and profile card download."""

from pathlib import Path

import config

from abdm_common.client import get_binary, post_json
from abdm_common.tokens import extract_x_token


def request_enrollment_otp(gateway_token: str, encrypted_login_id: str, **kwargs: object) -> str:
    payload = {
        "txnId": kwargs.get("txn_id", "") or "",
        "scope": kwargs.get("scope", ["abha-enrol"]),
        "loginHint": kwargs.get("login_hint", "aadhaar"),
        "loginId": encrypted_login_id,
        "otpSystem": kwargs.get("otp_system", "aadhaar"),
    }
    data = post_json(config.OTP_REQUEST_URL, payload, gateway_token=gateway_token)
    txn_id = data.get("txnId")
    if not txn_id:
        raise RuntimeError(f"OTP request response did not include txnId: {data}")
    return str(txn_id)


def enroll_by_aadhaar(
    gateway_token: str,
    txn_id: str,
    encrypted_otp: str,
    mobile_number: str,
) -> str:
    payload = {
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "txnId": txn_id,
                "otpValue": encrypted_otp,
                "mobile": mobile_number,
            },
        },
        "consent": {
            "code": "abha-enrollment",
            "version": "1.4",
        },
    }
    data = post_json(config.ENROLL_AADHAAR_URL, payload, gateway_token=gateway_token)
    x_token = extract_x_token(data)
    if not x_token:
        raise RuntimeError(f"Enrollment response did not include token: {data}")
    return x_token


def download_abha_card(gateway_token: str, x_token: str, output_base: str) -> Path:
    data, content_type = get_binary(
        config.ABHA_CARD_URL,
        gateway_token=gateway_token,
        x_token=x_token,
    )
    if not data:
        raise RuntimeError("ABHA card API returned an empty body.")
    output_path = Path(output_base)
    ct = content_type.lower()
    if "png" in ct:
        output_path = output_path.with_suffix(".png")
    elif "pdf" in ct:
        output_path = output_path.with_suffix(".pdf")
    else:
        output_path = output_path.with_suffix(".bin")
    output_path.write_bytes(data)
    return output_path
