#!/usr/bin/env python3
"""Enrollment via Aadhaar biometrics (Postman: ABHA Enrollment via Biometrics).

Sends POST to /enrollment/enrol/byAadhaar with a JSON body (face/iris/fingerprint
PID data). Build the body per NHA/ABDM spec or from Postman examples.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from abdm_common import extract_x_token, fetch_gateway_token, load_state, post_json, save_state
import config


def main() -> None:
    p = argparse.ArgumentParser(description="Biometric enrollment (byAadhaar body from file).")
    p.add_argument(
        "--body",
        type=Path,
        required=True,
        help="JSON request body (authData with face/fingerprint/iris per API spec)",
    )
    p.add_argument("--gateway-token")
    args = p.parse_args()

    gt = args.gateway_token or load_state().get("gateway_token")
    if not gt:
        gt = fetch_gateway_token()

    payload = json.loads(args.body.read_text(encoding="utf-8"))
    data = post_json(config.ENROLL_AADHAAR_URL, payload, gateway_token=gt)
    xt = extract_x_token(data)
    if xt:
        st = load_state()
        st.update({"gateway_token": gt, "x_token": xt})
        save_state(st)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
