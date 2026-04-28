# ABDM Use Case Flow Diagrams

These diagrams show **what to call next** and the dependency tokens (`gatewayToken`, `txnId`, `xToken`) required between API calls.

---

## 1) Common Foundation (used by most flows)

```mermaid
flowchart TD
  start[Start]
  session["POST /api/hiecm/gateway/v3/sessions"]
  gatewayToken[gatewayToken]
  start --> session --> gatewayToken
```

---

## 2) Aadhaar Enrollment -> ABHA Card

```mermaid
flowchart TD
  session["POST /api/hiecm/gateway/v3/sessions"]
  reqOtp["POST /abha/api/v3/enrollment/request/otp"]
  txnId[txnId]
  enroll["POST /abha/api/v3/enrollment/enrol/byAadhaar"]
  xToken[xToken]
  card["GET /abha/api/v3/profile/account/abha-card"]
  done[Card downloaded]

  session --> reqOtp --> txnId --> enroll --> xToken --> card --> done
```

Dependencies:
- `request/otp` needs encrypted Aadhaar + `gatewayToken`
- `enrol/byAadhaar` needs `txnId` + encrypted OTP + mobile + `gatewayToken`
- `abha-card` needs `gatewayToken` + `xToken`

---

## 3) Verification / Login Flows

```mermaid
flowchart TD
  session["POST /api/hiecm/gateway/v3/sessions"]

  reqOtpAadhaar["POST /abha/api/v3/profile/login/request/otp (aadhaar)"]
  reqOtpAbha["POST /abha/api/v3/profile/login/request/otp (abha-number)"]
  txnId[txnId]
  verifyOtp["POST /abha/api/v3/profile/login/verify (otp)"]
  xToken1[xToken]

  search["POST /abha/api/v3/profile/login/search"]
  verifyPwd["POST /abha/api/v3/profile/login/verify (password)"]
  xToken2[xToken]

  verifyUser["POST /abha/api/v3/profile/login/verify/user"]

  session --> reqOtpAadhaar --> txnId --> verifyOtp --> xToken1
  session --> reqOtpAbha --> txnId
  session --> search
  session --> verifyPwd --> xToken2
  session --> verifyUser
```

Dependencies:
- OTP verify branch uses `txnId` from request-otp
- Password branch does not need OTP txn
- `verify/user` may require `T-token` in header depending on context

---

## 4) Forgot / Retrieval

```mermaid
flowchart TD
  session["POST /api/hiecm/gateway/v3/sessions"]
  reqOtp["POST /abha/api/v3/profile/login/request/otp"]
  txnId[txnId]
  verify["POST /abha/api/v3/profile/login/verify"]
  result[Account / retrieval result]

  session --> reqOtp --> txnId --> verify --> result
```

Note: Same underlying APIs as verification OTP flow.

---

## 5) Profile Flows

```mermaid
flowchart TD
  session["POST /api/hiecm/gateway/v3/sessions"]
  loginOrEnroll["Verification or Enrollment flow"]
  xToken[xToken]

  profile["GET /abha/api/v3/profile/account"]
  card["GET /abha/api/v3/profile/account/abha-card"]
  emailLink["POST /abha/api/v3/profile/account/request/emailVerificationLink"]

  session --> loginOrEnroll --> xToken
  xToken --> profile
  xToken --> card
  xToken --> emailLink
```

Dependencies:
- Profile APIs are typically post-login/post-enroll operations requiring `xToken`

---

## 6) DL Enrollment Flow

```mermaid
flowchart TD
  sessionV05["POST /gateway/v0.5/sessions"]
  reqOtp["POST /abha/api/v3/enrollment/request/otp (mobile dl-flow)"]
  txnId[txnId]
  authByAbdm["POST /abha/api/v3/enrollment/auth/byAbdm"]
  enrollDoc["POST /abha/api/v3/enrollment/enrol/byDocument"]
  maybeXToken[xToken if returned]

  sessionV05 --> reqOtp --> txnId --> authByAbdm --> enrollDoc --> maybeXToken
```

Dependencies:
- `enrol/byDocument` body contains DL and identity details
- `auth/byAbdm` needs OTP + txn chain from request-otp

---

## 7) Biometric Enrollment

```mermaid
flowchart TD
  session["POST /api/hiecm/gateway/v3/sessions"]
  enrollBio["POST /abha/api/v3/enrollment/enrol/byAadhaar (face/fingerprint/iris body)"]
  maybeXToken[xToken if returned]

  session --> enrollBio --> maybeXToken
```

Dependencies:
- Requires API-spec compliant biometric payload/PID block

---

## 8) Benefit APIs

```mermaid
flowchart TD
  session["POST /api/hiecm/gateway/v3/sessions"]
  loginOrEnroll["Verification/Enrollment to obtain xToken"]
  xToken[xToken]
  link["POST /abha/api/v3/profile/benefit/linkAndDelink"]
  search["POST /abha/api/v3/profile/benefit/search"]
  getByAbha["GET /abha/api/v3/profile/benefit/abha/{abha}"]

  session --> loginOrEnroll --> xToken
  xToken --> link
  xToken --> search
  xToken --> getByAbha
```

Dependencies:
- Usually requires authenticated profile context (`xToken`)

---

## 9) Scan and Share / Gateway Ops

```mermaid
flowchart TD
  session["POST /api/hiecm/gateway/v3/sessions"]
  patchBridge["PATCH /api/hiecm/gateway/v3/bridge/url"]
  certs["GET /api/hiecm/gateway/v3/certs"]
  openid["GET /api/hiecm/gateway/v3/.well-known/openid-configuration"]
  onShare["POST /api/hiecm/patient-share/v3/on-share"]

  session --> patchBridge
  session --> certs
  session --> openid
  session --> onShare
```

Dependencies:
- Most gateway/bridge calls require gateway bearer token

---

## Token Dependency Quick View

```mermaid
flowchart LR
  session["Session API"] --> gatewayToken[gatewayToken]
  reqOtp["Request OTP APIs"] --> txnId[txnId]
  verifyOrEnroll["Verify/Enroll APIs"] --> xToken[xToken]

  gatewayToken --> reqOtp
  gatewayToken --> verifyOrEnroll
  txnId --> verifyOrEnroll
  xToken --> profileBenefitCard["Profile / Benefit / Card APIs"]
```

