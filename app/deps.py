from fastapi import HTTPException, Header
from typing import Optional
from app.auth import decode_token


def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated. Please log in.")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    return payload
