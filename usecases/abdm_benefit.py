#!/usr/bin/env python3
"""Benefit link/search APIs (Postman: BENEFIT_APIS)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from abdm_common import fetch_gateway_token, get_json, load_state, post_json
from abdm_common.settings import resolve_url, current_env
import config


def main() -> None:
    p = argparse.ArgumentParser(description="ABHA benefit link / search.")
    p.add_argument(
        "--flow",
        required=True,
        choices=("link", "search", "get-by-abha"),
    )
    p.add_argument("--gateway-token")
    p.add_argument("--x-token", help="Profile token after login")
    p.add_argument(
        "--body",
        type=Path,
        help="JSON body for link or search (see Postman)",
    )
    p.add_argument(
        "--abha-number",
        help="For get-by-abha: ABHA number in path (no dashes or with)",
    )
    args = p.parse_args()

    gt = args.gateway_token or load_state().get("gateway_token")
    if not gt:
        gt = fetch_gateway_token()
    xt = args.x_token or load_state().get("x_token")
    if args.flow in ("link", "search") and not xt:
        sys.exit("--x-token required (benefit APIs need profile session token)")

    if args.flow == "link" or args.flow == "search":
        if not args.body:
            sys.exit("--body JSON file required")
        body = json.loads(args.body.read_text(encoding="utf-8"))
        url = config.BENEFIT_LINK_URL if args.flow == "link" else config.BENEFIT_SEARCH_URL
        out = post_json(url, body, gateway_token=gt, x_token=xt)
    else:
        if not args.abha_number:
            sys.exit("--abha-number required")
        num = args.abha_number.replace("-", "")
        url = resolve_url(
            f"https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/abha/{num}",
            current_env(),
        )
        out = get_json(url, gateway_token=gt, x_token=xt)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
