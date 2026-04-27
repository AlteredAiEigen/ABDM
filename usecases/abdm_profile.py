#!/usr/bin/env python3
"""ABHA Profile APIs (Postman: ABHA Profile)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from abdm_common import download_abha_card, get_json, load_state, post_json, fetch_gateway_token
import config


def _tokens(args: argparse.Namespace) -> tuple[str, str | None]:
    gt = args.gateway_token or load_state().get("gateway_token")
    if not gt:
        gt = fetch_gateway_token()
    xt = args.x_token or load_state().get("x_token")
    return gt, xt


def main() -> None:
    p = argparse.ArgumentParser(description="ABHA profile (account, card, email link).")
    p.add_argument(
        "--flow",
        required=True,
        choices=("get-profile", "download-card", "email-verification-link"),
    )
    p.add_argument("--gateway-token")
    p.add_argument("--x-token")
    p.add_argument("-o", "--output", default="ABHA_card/abha-card", help="For download-card")
    p.add_argument(
        "--body",
        type=Path,
        help="JSON file for email-verification-link request body (if not using defaults)",
    )
    args = p.parse_args()
    gt, xt = _tokens(args)

    if args.flow == "get-profile":
        if not xt:
            sys.exit("--x-token or session x_token required for get-profile")
        out = get_json(
            config.PROFILE_ACCOUNT_URL,
            gateway_token=gt,
            x_token=xt,
        )
    elif args.flow == "download-card":
        if not xt:
            sys.exit("--x-token or session x_token required")
        path = download_abha_card(gt, xt, args.output)
        out = {"path": str(path)}
    else:
        body: dict
        if args.body:
            body = json.loads(args.body.read_text(encoding="utf-8"))
        else:
            body = {}
        if not xt:
            sys.exit("--x-token or session x_token required")
        out = post_json(
            config.EMAIL_VERIFICATION_LINK_URL,
            body,
            gateway_token=gt,
            x_token=xt,
        )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
