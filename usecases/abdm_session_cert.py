#!/usr/bin/env python3
"""Gateway session + public certificate (ABDM Session and cert API)."""

from __future__ import annotations

import argparse
import json
import sys

from abdm_common import (
    current_env,
    fetch_gateway_token,
    fetch_public_certificate,
    load_state,
    post_json,
    save_state,
)
import config


def run_token() -> dict:
    t = fetch_gateway_token()
    st = load_state()
    st["gateway_token"] = t
    save_state(st)
    return {"accessToken": t, "environment": current_env()}


def run_certificate(gateway_token: str | None) -> dict:
    gt = gateway_token or load_state().get("gateway_token")
    if not gt:
        gt = fetch_gateway_token()
    data = fetch_public_certificate(gateway_token=gt)
    return data


def run_session_raw_v3() -> dict:
    return post_json(
        config.SESSION_URL,
        {
            "clientId": config.CLIENT_ID,
            "clientSecret": config.CLIENT_SECRET,
            "grantType": config.GRANT_TYPE,
        },
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Session API and public certificate fetch.")
    p.add_argument(
        "--flow",
        required=True,
        choices=("token", "certificate", "public-key", "session-raw"),
        help="token: fetch gateway token; certificate: full cert JSON; public-key: only publicKey field; session-raw: full session response",
    )
    p.add_argument("--json", action="store_true")
    p.add_argument(
        "--write-key",
        metavar="FILE",
        help="With public-key, write base64 public key to FILE (e.g. for ABDM_PUBLIC_KEY_B64)",
    )
    p.add_argument(
        "--gateway-token",
        help="Bearer for certificate call (default: fetch new or use state)",
    )
    args = p.parse_args()

    if args.flow == "token":
        out = run_token()
    elif args.flow == "session-raw":
        out = run_session_raw_v3()
    elif args.flow == "certificate":
        out = run_certificate(args.gateway_token)
    else:
        cert = run_certificate(args.gateway_token)
        pk = cert.get("publicKey")
        if not pk:
            sys.exit(f"No publicKey in response: {cert}")
        if args.write_key:
            path = args.write_key
            with open(path, "w", encoding="utf-8") as f:
                f.write(pk)
            out = {"publicKey": pk, "written": path}
        else:
            out = {"publicKey": pk}

    if args.json or args.flow == "public-key":
        print(json.dumps(out, indent=2))
    else:
        print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
