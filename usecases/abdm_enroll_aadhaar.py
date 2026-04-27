#!/usr/bin/env python3
"""ABHA enrollment via Aadhaar OTP (Postman: ABHA enrolment via Aadhaar)."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from abdm_common import (
    clear_state,
    download_abha_card,
    enroll_by_aadhaar,
    encrypt_with_public_key,
    fetch_gateway_token,
    load_state,
    request_enrollment_otp,
    save_state,
)
import config


def _prompt(label: str, secret: bool = False) -> str:
    if secret:
        import getpass

        return getpass.getpass(f"{label}: ").strip()
    return input(f"{label}: ").strip()


def _out(data: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2))
    else:
        if isinstance(data, dict):
            for k, v in data.items():
                print(f"{k}: {v}")
        else:
            print(data)


def flow_request_otp(
    args: argparse.Namespace,
) -> dict[str, Any]:
    gt = args.gateway_token or load_state().get("gateway_token")
    if not gt:
        gt = fetch_gateway_token()
    enc = encrypt_with_public_key(args.aadhaar)
    txn_id = request_enrollment_otp(gt, enc)
    st = load_state()
    st.update(
        {
            "gateway_token": gt,
            "txn_id": txn_id,
            "mobile": args.mobile,
        }
    )
    save_state(st)
    return {"gateway_token": gt, "txnId": txn_id, "mobile": args.mobile}


def flow_enrol(args: argparse.Namespace) -> dict[str, Any]:
    st = load_state()
    gt = args.gateway_token or st.get("gateway_token")
    txn_id = args.txn_id or st.get("txn_id")
    mobile = args.mobile or st.get("mobile")
    if not gt or not txn_id or not mobile:
        sys.exit("Missing gateway token, txnId, or mobile. Run request-otp first or pass flags.")
    enc_otp = encrypt_with_public_key(args.otp)
    x_token = enroll_by_aadhaar(gt, txn_id, enc_otp, mobile)
    st = load_state()
    st.update({"gateway_token": gt, "x_token": x_token})
    save_state(st)
    return {"x_token": x_token}


def flow_card(args: argparse.Namespace) -> dict[str, Any]:
    st = load_state()
    gt = args.gateway_token or st.get("gateway_token")
    xt = args.x_token or st.get("x_token")
    if not gt or not xt:
        sys.exit("Need gateway token and X-Token (enrol first or pass --gateway-token / --x-token).")
    out = args.output or "ABHA_card/abha-card"
    path = download_abha_card(gt, xt, out)
    return {"path": str(path)}


def flow_full(args: argparse.Namespace) -> dict[str, Any]:
    aadhaar = args.aadhaar or _prompt("Aadhaar number")
    mobile = args.mobile or _prompt("Mobile number")
    gt = fetch_gateway_token()
    txn_id = request_enrollment_otp(gt, encrypt_with_public_key(aadhaar))
    otp = args.otp or _prompt("OTP received", secret=True)
    if not otp:
        sys.exit("OTP required")
    enc_otp = encrypt_with_public_key(otp)
    x_token = enroll_by_aadhaar(gt, txn_id, enc_otp, mobile)
    path = download_abha_card(gt, x_token, args.output or "ABHA_card/abha-card")
    st = load_state()
    st.update({"gateway_token": gt, "x_token": x_token})
    save_state(st)
    return {
        "txnId": txn_id,
        "x_token": x_token,
        "card_path": str(path),
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="ABDM ABHA enrollment via Aadhaar (sandbox/prod via ABDM_ENV).")
    p.add_argument(
        "--flow",
        required=True,
        choices=("request-otp", "enrol", "card", "full"),
        help="request-otp: get txnId; enrol: verify OTP; card: download card; full: end-to-end",
    )
    p.add_argument("--json", action="store_true", help="Print JSON result")
    p.add_argument("--output", "-o", help="Output file base for card (default: ABHA_card/abha-card)")
    p.add_argument("--gateway-token", help="Override gateway access token")
    p.add_argument("--x-token", help="Profile X-Token (for --flow card)")
    p.add_argument("--aadhaar", help="Aadhaar (request-otp or full)")
    p.add_argument("--mobile", help="Mobile number")
    p.add_argument("--txn-id", dest="txn_id", help="Transaction id (enrol)")
    p.add_argument("--otp", help="OTP (enrol or full)")
    p.add_argument(
        "--clear-state",
        action="store_true",
        help="Clear stored session file before this run",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()
    if args.clear_state:
        clear_state()
    if args.flow == "request-otp":
        if not args.aadhaar or not args.mobile:
            sys.exit("--aadhaar and --mobile are required for request-otp (non-full).")
        r = flow_request_otp(args)
    elif args.flow == "enrol":
        if not args.otp:
            sys.exit("--otp is required for enrol")
        r = flow_enrol(args)
    elif args.flow == "card":
        r = flow_card(args)
    else:
        r = flow_full(args)
    _out(r, args.json)
    if not args.json and args.flow != "card":
        print(f"Environment: {getattr(config, 'ABDM_ENV', 'sandbox')}, state: ~/.abdm_session.json (or ABDM_STATE_FILE)")


if __name__ == "__main__":
    main()
