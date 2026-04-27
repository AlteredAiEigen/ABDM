#!/usr/bin/env python3
"""Forgot ABHA & enrollment retrieval (Postman: Forgot ABHA & Retrieval).

Uses the same /profile/login/request/otp and /verify endpoints as
`abdm_verification.py`; this file is a convenience entry point.
"""

from usecases.abdm_verification import main

if __name__ == "__main__":
    main()
