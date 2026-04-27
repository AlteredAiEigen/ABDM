"""RSA OAEP SHA-1 encryption (Java: RSA/ECB/OAEPWithSHA-1AndMGF1Padding)."""

import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA

from abdm_common.settings import get_public_key_b64


def encrypt_with_public_key(value: str) -> str:
    der = base64.b64decode(get_public_key_b64())
    rsa_key = RSA.import_key(der)
    cipher = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA1)
    encrypted = cipher.encrypt(value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")
