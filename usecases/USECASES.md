# ABDM Use Cases (Terminal Commands)

Run from project root:

```bash
cd /Users/chanpreetsingh/ABDM
```

## `abdm_session_cert.py`

```bash
# show help
./.venv/bin/python -m usecases.abdm_session_cert --help

# flow: token
./.venv/bin/python -m usecases.abdm_session_cert --flow token --json

# flow: certificate
./.venv/bin/python -m usecases.abdm_session_cert --flow certificate --json

# flow: public-key
./.venv/bin/python -m usecases.abdm_session_cert --flow public-key --json

# flow: public-key and write to file
./.venv/bin/python -m usecases.abdm_session_cert --flow public-key --write-key /tmp/abdm_pub.b64

# flow: session-raw
./.venv/bin/python -m usecases.abdm_session_cert --flow session-raw --json
```

## `abdm_enroll_aadhaar.py`

```bash
# show help
./.venv/bin/python -m usecases.abdm_enroll_aadhaar --help

# flow: request-otp
./.venv/bin/python -m usecases.abdm_enroll_aadhaar --flow request-otp --aadhaar 123456789012 --mobile 9876543210 --json

# flow: enrol (uses txnId from state by default)
./.venv/bin/python -m usecases.abdm_enroll_aadhaar --flow enrol --otp 123456 --json

# flow: card (downloads to ABHA_card by default)
./.venv/bin/python -m usecases.abdm_enroll_aadhaar --flow card --json

# flow: full (interactive end-to-end)
./.venv/bin/python -m usecases.abdm_enroll_aadhaar --flow full

# optional: clear local state before run
./.venv/bin/python -m usecases.abdm_enroll_aadhaar --flow full --clear-state
```

## `abdm_flow.py` (legacy wrapper)

```bash
# interactive full flow (same as abdm_enroll_aadhaar full)
./.venv/bin/python -m usecases.abdm_flow
```

## `abdm_enroll_dl.py`

```bash
# show help
./.venv/bin/python -m usecases.abdm_enroll_dl --help

# flow: session-v05
./.venv/bin/python -m usecases.abdm_enroll_dl --flow session-v05

# flow: request-otp
./.venv/bin/python -m usecases.abdm_enroll_dl --flow request-otp --mobile 9876543210

# flow: auth-abdm
./.venv/bin/python -m usecases.abdm_enroll_dl --flow auth-abdm --otp 123456

# flow: enrol-document (body from file)
./.venv/bin/python -m usecases.abdm_enroll_dl --flow enrol-document --body ./dl-enrol.json
```

## `abdm_enroll_biometric.py`

```bash
# show help
./.venv/bin/python -m usecases.abdm_enroll_biometric --help

# body-driven biometric enrollment
./.venv/bin/python -m usecases.abdm_enroll_biometric --body ./biometric-enrol.json
```

## `abdm_verification.py`

```bash
# show help
./.venv/bin/python -m usecases.abdm_verification --help

# flow: request-otp-aadhaar
./.venv/bin/python -m usecases.abdm_verification --flow request-otp-aadhaar --aadhaar 123456789012

# flow: request-otp-abha
./.venv/bin/python -m usecases.abdm_verification --flow request-otp-abha --abha-number 91-1234-5678-9012

# flow: verify-otp
./.venv/bin/python -m usecases.abdm_verification --flow verify-otp --otp 123456

# flow: password
./.venv/bin/python -m usecases.abdm_verification --flow password --abha-number 91-1234-5678-9012 --password '***'

# flow: search
./.venv/bin/python -m usecases.abdm_verification --flow search --abha-number 91-1234-5678-9012

# flow: verify-user
./.venv/bin/python -m usecases.abdm_verification --flow verify-user --abha-number 91-1234-5678-9012 --txn-id <TXN_ID> --t-token "Bearer <TOKEN>"
```

## `abdm_forgot_retrieve.py`

```bash
# same CLI options/flows as abdm_verification
./.venv/bin/python -m usecases.abdm_forgot_retrieve --help
./.venv/bin/python -m usecases.abdm_forgot_retrieve --flow request-otp-aadhaar --aadhaar 123456789012
./.venv/bin/python -m usecases.abdm_forgot_retrieve --flow verify-otp --otp 123456
```

## `abdm_profile.py`

```bash
# show help
./.venv/bin/python -m usecases.abdm_profile --help

# flow: get-profile
./.venv/bin/python -m usecases.abdm_profile --flow get-profile --x-token "<X_TOKEN>"

# flow: download-card (default path ABHA_card/abha-card.*)
./.venv/bin/python -m usecases.abdm_profile --flow download-card --x-token "<X_TOKEN>"

# flow: email-verification-link (optional body file)
./.venv/bin/python -m usecases.abdm_profile --flow email-verification-link --x-token "<X_TOKEN>" --body ./email-link-body.json
```

## `abdm_benefit.py`

```bash
# show help
./.venv/bin/python -m usecases.abdm_benefit --help

# flow: link
./.venv/bin/python -m usecases.abdm_benefit --flow link --x-token "<X_TOKEN>" --body ./benefit-link.json

# flow: search
./.venv/bin/python -m usecases.abdm_benefit --flow search --x-token "<X_TOKEN>" --body ./benefit-search.json

# flow: get-by-abha
./.venv/bin/python -m usecases.abdm_benefit --flow get-by-abha --x-token "<X_TOKEN>" --abha-number 91-1234-5678-9012
```

## `abdm_scan_share.py`

```bash
# show help
./.venv/bin/python -m usecases.abdm_scan_share --help

# flow: patch-bridge-url
./.venv/bin/python -m usecases.abdm_scan_share --flow patch-bridge-url --body ./bridge-url.json

# flow: patient-on-share
./.venv/bin/python -m usecases.abdm_scan_share --flow patient-on-share --body ./on-share.json

# flow: certs
./.venv/bin/python -m usecases.abdm_scan_share --flow certs

# flow: openid-config
./.venv/bin/python -m usecases.abdm_scan_share --flow openid-config
```

## Notes

- Shared runtime logic is in `abdm_common/`.
- Configuration and env overrides are in `config.py`.
- Session state default: `~/.abdm_session.json` (override via `ABDM_STATE_FILE`).
- Downloaded cards default to `ABHA_card/`.
