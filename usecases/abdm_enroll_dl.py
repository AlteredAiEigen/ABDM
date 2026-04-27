#!/usr/bin/env python3
"""ABHA enrollment via Driving Licence (Postman: ABHA Enrolment via DL).

Uses gateway v0.5 session for some steps, then enrollment APIs.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from abdm_common import (
    encrypt_with_public_key,
    extract_x_token,
    fetch_gateway_token,
    fetch_gateway_token_v05,
    load_state,
    post_json,
    save_state,
)
import config


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def flow_session_v05(_: argparse.Namespace) -> dict:
    t = fetch_gateway_token_v05()
    st = load_state()
    st["gateway_token"] = t
    st["dl_session"] = "v0.5"
    save_state(st)
    return {"accessToken": t, "session": "v0.5"}


def flow_request_otp(args: argparse.Namespace) -> dict:
    gt = args.gateway_token or load_state().get("gateway_token") or fetch_gateway_token()
    if not args.mobile:
        sys.exit("--mobile required (10-digit mobile)")
    mobile = "".join(c for c in args.mobile if c.isdigit())
    payload = {
        "scope": ["abha-enrol", "mobile-verify", "dl-flow"],
        "loginHint": "mobile",
        "loginId": encrypt_with_public_key(mobile),
        "otpSystem": "abdm",
    }
    data = post_json(config.OTP_REQUEST_URL, payload, gateway_token=gt)
    st = load_state()
    st.update({"gateway_token": gt, "dl_txn_id": data.get("txnId")})
    save_state(st)
    return data


def flow_auth_abdm(args: argparse.Namespace) -> dict:
    gt = args.gateway_token or load_state().get("gateway_token")
    st = load_state()
    txn_id = args.txn_id or st.get("dl_txn_id")
    if not gt or not txn_id or not args.otp:
        sys.exit("Need gateway token, txn id (from request-otp), and --otp")
    payload = {
        "scope": ["abha-enrol", "mobile-verify"],
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "timeStamp": _ts(),
                "txnId": txn_id,
                "otpValue": encrypt_with_public_key(args.otp),
            },
        },
    }
    return post_json(config.AUTH_BY_ABDM_URL, payload, gateway_token=gt)


def flow_enrol_document(args: argparse.Namespace) -> dict:
    gt = args.gateway_token or load_state().get("gateway_token")
    if not gt:
        sys.exit("Gateway token required")
    if not args.body:
        sys.exit("--body JSON file required (see Postman Create Enrolment Number)")
    body = json.loads(args.body.read_text(encoding="utf-8"))
    data = post_json(config.ENROLL_BY_DOCUMENT_URL, body, gateway_token=gt)
    xt = extract_x_token(data)
    if xt:
        st = load_state()
        st["x_token"] = xt
        save_state(st)
    return data


def main() -> None:
    p = argparse.ArgumentParser(description="DL-based ABHA enrollment.")
    p.add_argument(
        "--flow",
        required=True,
        choices=("session-v05", "request-otp", "auth-abdm", "enrol-document"),
    )
    p.add_argument("--gateway-token")
    p.add_argument("--mobile")
    p.add_argument("--otp")
    p.add_argument("--txn-id", dest="txn_id")
    p.add_argument("--body", type=Path, help="JSON for enrol-document")
    args = p.parse_args()
    if args.flow == "session-v05":
        out = flow_session_v05(args)
    elif args.flow == "request-otp":
        out = flow_request_otp(args)
    elif args.flow == "auth-abdm":
        out = flow_auth_abdm(args)
    else:
        out = flow_enrol_document(args)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
