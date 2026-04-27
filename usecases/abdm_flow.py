#!/usr/bin/env python3
"""Backward-compatible entry: interactive full enrollment + re-exports for ui_app."""

import json

from abdm_common import (
    download_abha_card,
    encrypt_with_public_key,
    enroll_by_aadhaar,
    fetch_gateway_token,
    request_enrollment_otp,
)
from usecases.abdm_enroll_aadhaar import flow_full


def request_aadhaar_otp(gateway_token: str, encrypted_aadhaar: str) -> str:
    return request_enrollment_otp(gateway_token, encrypted_aadhaar)


def main() -> None:
    print("ABDM robust flow started.")
    print("(Tip: use python -m usecases.abdm_enroll_aadhaar --flow full --json)")
    ns = type(
        "NS",
        (),
        {
            "aadhaar": None,
            "mobile": None,
            "otp": None,
            "output": "ABHA_card/abha-card",
            "gateway_token": None,
            "x_token": None,
            "txn_id": None,
        },
    )()
    result = flow_full(ns)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
