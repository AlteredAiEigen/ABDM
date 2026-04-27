#!/usr/bin/env python3
"""Scan and Share / gateway bridge (Postman: Scan and Share)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from abdm_common import fetch_gateway_token, get_json, load_state, patch_json, post_json
import config


def main() -> None:
    p = argparse.ArgumentParser(description="HIE-CM gateway bridge + patient share.")
    p.add_argument(
        "--flow",
        required=True,
        choices=("patch-bridge-url", "patient-on-share", "certs", "openid-config"),
    )
    p.add_argument("--gateway-token")
    p.add_argument(
        "--body",
        type=Path,
        help="JSON body for PATCH bridge or POST on-share",
    )
    args = p.parse_args()

    gt = args.gateway_token or load_state().get("gateway_token")
    if not gt:
        gt = fetch_gateway_token()

    if args.flow == "patch-bridge-url":
        if not args.body:
            sys.exit("--body required")
        body = json.loads(args.body.read_text(encoding="utf-8"))
        out = patch_json(config.GATEWAY_BRIDGE_URL, body, gateway_token=gt)
    elif args.flow == "patient-on-share":
        if not args.body:
            sys.exit("--body required")
        body = json.loads(args.body.read_text(encoding="utf-8"))
        out = post_json(config.PATIENT_ON_SHARE_URL, body, gateway_token=gt)
    elif args.flow == "certs":
        url = "https://dev.abdm.gov.in/api/hiecm/gateway/v3/certs"
        out = get_json(url, gateway_token=gt)
    else:
        url = "https://dev.abdm.gov.in/api/hiecm/gateway/v3/.well-known/openid-configuration"
        out = get_json(url, gateway_token=gt)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
