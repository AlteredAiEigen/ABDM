# ABDM Use Case Scripts

All ABDM workflow scripts are grouped in this folder.

Run scripts as Python modules from the project root:

```bash
cd /Users/chanpreetsingh/ABDM
./.venv/bin/python -m usecases.<script_name> --help
```

## Scripts

- `abdm_session_cert.py`
  - Session and certificate operations.
  - Flows: `token`, `certificate`, `public-key`, `session-raw`.

- `abdm_enroll_aadhaar.py`
  - Aadhaar-based ABHA enrollment flow.
  - Flows: `request-otp`, `enrol`, `card`, `full`.
  - Example:
    - `./.venv/bin/python -m usecases.abdm_enroll_aadhaar --flow full`
  - Card output default: `ABHA_card/abha-card.(png|pdf|bin)`.

- `abdm_flow.py`
  - Backward-compatible interactive wrapper for full Aadhaar flow.
  - Uses `abdm_enroll_aadhaar.py` internally.

- `abdm_enroll_dl.py`
  - Driving Licence enrollment workflow.
  - Flows: `session-v05`, `request-otp`, `auth-abdm`, `enrol-document`.
  - `enrol-document` expects `--body` JSON file.

- `abdm_enroll_biometric.py`
  - Biometric-based enrollment (`byAadhaar`) using raw JSON body file.
  - Requires `--body` JSON.

- `abdm_verification.py`
  - ABHA verification/login workflows.
  - Flows:
    - `request-otp-aadhaar`
    - `request-otp-abha`
    - `verify-otp`
    - `password`
    - `search`
    - `verify-user`

- `abdm_forgot_retrieve.py`
  - Convenience entry for forgot/retrieval style login OTP verification.
  - Delegates to verification script behavior.

- `abdm_profile.py`
  - Profile account operations.
  - Flows: `get-profile`, `download-card`, `email-verification-link`.
  - Requires `X-Token` for profile-secured calls.
  - `download-card` default output: `ABHA_card/abha-card.(png|pdf|bin)`.

- `abdm_benefit.py`
  - Benefit APIs.
  - Flows: `link`, `search`, `get-by-abha`.
  - `link` and `search` use `--body` JSON.

- `abdm_scan_share.py`
  - Scan and Share / gateway bridge utilities.
  - Flows: `patch-bridge-url`, `patient-on-share`, `certs`, `openid-config`.
  - `patch-bridge-url` and `patient-on-share` use `--body` JSON.

## Notes

- Shared logic is in `abdm_common/` (HTTP, crypto, state, URL env resolution).
- Config defaults and env overrides are in `config.py`.
- Session state is stored in `~/.abdm_session.json` unless `ABDM_STATE_FILE` is set.
- Downloaded cards are stored in `ABHA_card/` by default.
