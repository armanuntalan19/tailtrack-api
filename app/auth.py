from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY         = os.getenv("SECRET_KEY", "changethisbeforegoingtoprduction123!")
ALGORITHM          = "HS256"
TOKEN_EXPIRE_HOURS = 8


def verify_password(plain: str, stored: str) -> bool:
    return plain == stored


def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
