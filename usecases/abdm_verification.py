#!/usr/bin/env python3
"""ABHA verification / login flows (Postman: ABHA Verification)."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from abdm_common import (
    encrypt_with_public_key,
    extract_x_token,
    fetch_gateway_token,
    load_state,
    post_json,
    save_state,
)
import config


def _gt(args: argparse.Namespace) -> str:
    t = args.gateway_token or load_state().get("gateway_token")
    if not t:
        t = fetch_gateway_token()
    return t


def flow_request_otp_aadhaar(args: argparse.Namespace) -> dict[str, Any]:
    gt = _gt(args)
    if not args.aadhaar:
        sys.exit("--aadhaar is required")
    payload = {
        "scope": ["abha-login", "aadhaar-verify"],
        "loginHint": "aadhaar",
        "loginId": encrypt_with_public_key(args.aadhaar),
        "otpSystem": "aadhaar",
    }
    data = post_json(config.LOGIN_REQUEST_OTP_URL, payload, gateway_token=gt)
    txn = data.get("txnId")
    st = load_state()
    st.update({"gateway_token": gt, "login_txn_id": txn, "verify_mode": "aadhaar-otp"})
    save_state(st)
    return data


def flow_request_otp_abha(args: argparse.Namespace) -> dict[str, Any]:
    gt = _gt(args)
    if not args.abha_number:
        sys.exit("--abha-number is required (format e.g. 91-XXXX-XXXX-XXXX)")
    digits = "".join(c for c in args.abha_number if c.isdigit())
    payload = {
        "scope": ["abha-login", "aadhaar-verify"],
        "loginHint": "abha-number",
        "loginId": encrypt_with_public_key(digits),
        "otpSystem": "aadhaar",
    }
    data = post_json(config.LOGIN_REQUEST_OTP_URL, payload, gateway_token=gt)
    st = load_state()
    st.update({"gateway_token": gt, "login_txn_id": data.get("txnId"), "verify_mode": "abha-otp"})
    save_state(st)
    return data


def flow_verify_otp(args: argparse.Namespace) -> dict[str, Any]:
    gt = _gt(args)
    st = load_state()
    txn_id = args.txn_id or st.get("login_txn_id")
    if not txn_id or not args.otp:
        sys.exit("Need --txn-id (or prior request-otp in state) and --otp")
    payload = {
        "scope": ["abha-login", "aadhaar-verify"],
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "txnId": txn_id,
                "otpValue": encrypt_with_public_key(args.otp),
            },
        },
    }
    data = post_json(config.LOGIN_VERIFY_URL, payload, gateway_token=gt)
    xt = extract_x_token(data)
    if xt:
        st["x_token"] = xt
        save_state(st)
    return data


def flow_password(args: argparse.Namespace) -> dict[str, Any]:
    gt = _gt(args)
    if not args.abha_number or not args.password:
        sys.exit("--abha-number and --password required")
    payload = {
        "scope": ["abha-login", "password-verify"],
        "authData": {
            "authMethods": ["password"],
            "password": {
                "ABHANumber": args.abha_number,
                "password": encrypt_with_public_key(args.password),
            },
        },
    }
    data = post_json(config.LOGIN_VERIFY_URL, payload, gateway_token=gt)
    xt = extract_x_token(data)
    if xt:
        st = load_state()
        st["x_token"] = xt
        save_state(st)
    return data


def flow_search(args: argparse.Namespace) -> dict[str, Any]:
    gt = _gt(args)
    if not args.abha_number:
        sys.exit("--abha-number required")
    data = post_json(
        config.LOGIN_SEARCH_URL,
        {"ABHANumber": args.abha_number},
        gateway_token=gt,
    )
    return data


def flow_verify_user(args: argparse.Namespace) -> dict[str, Any]:
    """POST login/verify/user (may require T-token header from PHR)."""
    gt = _gt(args)
    if not args.abha_number or not args.txn_id:
        sys.exit("--abha-number and --txn-id required")
    body = {"ABHANumber": args.abha_number, "txnId": args.txn_id}
    extra = {}
    if args.t_token:
        extra["T-token"] = args.t_token
    return post_json(
        config.LOGIN_VERIFY_USER_URL,
        body,
        gateway_token=gt,
        extra_headers=extra,
    )


def dispatch_verification(args: argparse.Namespace) -> dict[str, Any]:
    if args.flow == "request-otp-aadhaar":
        return flow_request_otp_aadhaar(args)
    if args.flow == "request-otp-abha":
        return flow_request_otp_abha(args)
    if args.flow == "verify-otp":
        return flow_verify_otp(args)
    if args.flow == "password":
        return flow_password(args)
    if args.flow == "search":
        return flow_search(args)
    return flow_verify_user(args)


def main() -> None:
    p = argparse.ArgumentParser(description="ABHA login / verification APIs.")
    p.add_argument(
        "--flow",
        required=True,
        choices=(
            "request-otp-aadhaar",
            "request-otp-abha",
            "verify-otp",
            "password",
            "search",
            "verify-user",
        ),
    )
    p.add_argument("--json", action="store_true")
    p.add_argument("--gateway-token")
    p.add_argument("--aadhaar")
    p.add_argument("--abha-number")
    p.add_argument("--otp")
    p.add_argument("--password")
    p.add_argument("--txn-id", dest="txn_id")
    p.add_argument(
        "--t-token",
        help="T-token header value for verify-user (e.g. Bearer ...)",
    )
    args = p.parse_args()
    out = dispatch_verification(args)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
