# ABDM Terminal Cheat Sheet

Terminal-only usage for all use cases.

## Run Pattern

```bash
cd /Users/chanpreetsingh/ABDM
./.venv/bin/python -m usecases.<script> --help
```

## Required Env Vars

```bash
export ABDM_CLIENT_ID="..."
export ABDM_CLIENT_SECRET="..."
export ABDM_X_CM_ID="sbx"
export ABDM_ENV="sandbox"   # or prod
```

Optional:
- `ABDM_PUBLIC_KEY_B64`
- `ABDM_STATE_FILE`

## Quick Commands

```bash
# gateway token
./.venv/bin/python -m usecases.abdm_session_cert --flow token --json

# full Aadhaar flow (interactive)
./.venv/bin/python -m usecases.abdm_enroll_aadhaar --flow full

# verification by Aadhaar OTP
./.venv/bin/python -m usecases.abdm_verification --flow request-otp-aadhaar --aadhaar 123456789012
./.venv/bin/python -m usecases.abdm_verification --flow verify-otp --otp 123456
```

## Use Case -> API Mapping

### `usecases.abdm_session_cert`
- `token` / `session-raw` -> `POST /api/hiecm/gateway/v3/sessions`
- `certificate` / `public-key` -> `GET /abha/api/v3/profile/public/certificate`

### `usecases.abdm_enroll_aadhaar`
- `request-otp` -> `POST /abha/api/v3/enrollment/request/otp`
- `enrol` -> `POST /abha/api/v3/enrollment/enrol/byAadhaar`
- `card` -> `GET /abha/api/v3/profile/account/abha-card`
- `full` -> sequence of all above

### `usecases.abdm_flow`
- Wrapper around `usecases.abdm_enroll_aadhaar --flow full`

### `usecases.abdm_enroll_dl`
- `session-v05` -> `POST /gateway/v0.5/sessions`
- `request-otp` -> `POST /abha/api/v3/enrollment/request/otp`
- `auth-abdm` -> `POST /abha/api/v3/enrollment/auth/byAbdm`
- `enrol-document` -> `POST /abha/api/v3/enrollment/enrol/byDocument`

### `usecases.abdm_enroll_biometric`
- `--body` flow -> `POST /abha/api/v3/enrollment/enrol/byAadhaar`
  (body decides face/fingerprint/iris mode)

### `usecases.abdm_verification`
- `request-otp-aadhaar` -> `POST /abha/api/v3/profile/login/request/otp`
- `request-otp-abha` -> `POST /abha/api/v3/profile/login/request/otp`
- `verify-otp` -> `POST /abha/api/v3/profile/login/verify`
- `password` -> `POST /abha/api/v3/profile/login/verify`
- `search` -> `POST /abha/api/v3/profile/login/search`
- `verify-user` -> `POST /abha/api/v3/profile/login/verify/user`

### `usecases.abdm_forgot_retrieve`
- Delegates to `usecases.abdm_verification`
- Uses the same `/profile/login/request/otp` and `/profile/login/verify` APIs

### `usecases.abdm_profile`
- `get-profile` -> `GET /abha/api/v3/profile/account`
- `download-card` -> `GET /abha/api/v3/profile/account/abha-card`
- `email-verification-link` -> `POST /abha/api/v3/profile/account/request/emailVerificationLink`

### `usecases.abdm_benefit`
- `link` -> `POST /abha/api/v3/profile/benefit/linkAndDelink`
- `search` -> `POST /abha/api/v3/profile/benefit/search`
- `get-by-abha` -> `GET /abha/api/v3/profile/benefit/abha/{abha}`

### `usecases.abdm_scan_share`
- `patch-bridge-url` -> `PATCH /api/hiecm/gateway/v3/bridge/url`
- `patient-on-share` -> `POST /api/hiecm/patient-share/v3/on-share`
- `certs` -> `GET /api/hiecm/gateway/v3/certs`
- `openid-config` -> `GET /api/hiecm/gateway/v3/.well-known/openid-configuration`

## Output + State

- Card downloads default to `ABHA_card/abha-card.(pdf|png|bin)`
- State file default: `~/.abdm_session.json`
