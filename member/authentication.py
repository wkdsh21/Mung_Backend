import time

import jwt

# JWT
SECRET_KEY = "92424d57e87900cd12b3f8ae43d31a0bfcbd34ea1b0004767ad0f61ab8376803"
ALGORITHM = "HS256"


def encode_access_token(username: str) -> str:
    payload = {"username": username, "isa": int(time.time())}
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token
