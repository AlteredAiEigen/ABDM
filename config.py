"""ABDM configuration. Defaults are for local sandbox; override with env vars."""

import os

def _e(name: str, default: str) -> str:
    v = os.environ.get(name)
    return v if v is not None and v != "" else default

# Environment: sandbox | prod (used by abdm_common.resolve_url)
ABDM_ENV = _e("ABDM_ENV", "sandbox")

# Gateway session credentials (override in production)
CLIENT_ID = _e("ABDM_CLIENT_ID", "SBXID_024365")
CLIENT_SECRET = _e("ABDM_CLIENT_SECRET", "901378b8-d428-432f-aee5-3c927d4e323c")
GRANT_TYPE = _e("ABDM_GRANT_TYPE", "client_credentials")

# ABHA profile public key (base64 DER) from certificate API; or set ABDM_PUBLIC_KEY_B64
_PUBLIC_DEFAULT = (
    "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO4Xb+59KY"
    "Vm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9Nwgv7LRGq5uLczpZQD"
    "rU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u68ZRxSYGMPe4hb9XXKDVsgoSJaR"
    "NYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/"
    "I4lcbftib8cv7llkybtjX1AayfZp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/D"
    "ChytYgBTBTJFe7irDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/"
    "PnkNergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG0oKDy9l"
    "AOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXuiwO/1C8y56egzKSw44"
    "GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3o/WAdOyV3xSQ9dqLY5MEL4sJCGY1i"
    "JBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAlsIzQpnSVDUVEzv17grVAw078CAwEAAQ=="
)
PUBLIC_KEY_BASE64 = _e("ABDM_PUBLIC_KEY_B64", _PUBLIC_DEFAULT)

# Endpoints (hosts rewritten at runtime if ABDM_ENV changes; keep sandbox URLs as defaults)
SESSION_URL = _e("ABDM_SESSION_URL", "https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions")
SESSION_URL_V05 = _e("ABDM_SESSION_URL_V05", "https://dev.abdm.gov.in/gateway/v0.5/sessions")
PUBLIC_CERTIFICATE_URL = _e(
    "ABDM_PUBLIC_CERTIFICATE_URL",
    "https://abhasbx.abdm.gov.in/abha/api/v3/profile/public/certificate",
)
OTP_REQUEST_URL = _e("ABDM_OTP_REQUEST_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp")
ENROLL_AADHAAR_URL = _e("ABDM_ENROLL_AADHAAR_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar")
ENROLL_BY_DOCUMENT_URL = _e(
    "ABDM_ENROLL_BY_DOCUMENT_URL",
    "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byDocument",
)
AUTH_BY_ABDM_URL = _e(
    "ABDM_AUTH_BY_ABDM_URL",
    "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm",
)
ABHA_CARD_URL = _e("ABDM_ABHA_CARD_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha-card")
PROFILE_ACCOUNT_URL = _e("ABDM_PROFILE_ACCOUNT_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account")
EMAIL_VERIFICATION_LINK_URL = _e(
    "ABDM_EMAIL_VERIFICATION_LINK_URL",
    "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/emailVerificationLink",
)
LOGIN_REQUEST_OTP_URL = _e("ABDM_LOGIN_REQUEST_OTP_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp")
LOGIN_VERIFY_URL = _e("ABDM_LOGIN_VERIFY_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify")
LOGIN_SEARCH_URL = _e("ABDM_LOGIN_SEARCH_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/search")
LOGIN_VERIFY_USER_URL = _e("ABDM_LOGIN_VERIFY_USER_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify/user")
BENEFIT_LINK_URL = _e("ABDM_BENEFIT_LINK_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/linkAndDelink")
BENEFIT_SEARCH_URL = _e("ABDM_BENEFIT_SEARCH_URL", "https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/search")
GATEWAY_BRIDGE_URL = _e(
    "ABDM_GATEWAY_BRIDGE_URL",
    "https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge/url",
)
PATIENT_ON_SHARE_URL = _e(
    "ABDM_PATIENT_ON_SHARE_URL",
    "https://dev.abdm.gov.in/api/hiecm/patient-share/v3/on-share",
)

# Header constants
X_CM_ID = _e("ABDM_X_CM_ID", "sbx")

# Optional state file for multi-step CLIs
STATE_FILE = _e("ABDM_STATE_FILE", "")
