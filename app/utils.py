import base64
import hashlib
import hmac

SECRET = "test_secret"


def verify_signature(signature: str, body: str) -> bool:
    expected = hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).digest()
    expected_b64 = base64.b64encode(expected).decode()
    return hmac.compare_digest(signature, expected_b64)


def generate_signature_from_body(raw_body: str) -> str:
    digest = hmac.new(SECRET.encode(), raw_body.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()
