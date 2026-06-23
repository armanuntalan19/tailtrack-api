from fastapi import HTTPException, Header, Depends
from typing import Optional
from app.auth import decode_token


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated. Please log in.")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    return payload


def admin_only(payload: dict = Depends(get_current_user)) -> dict:
    if (payload.get("role") or "").upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Access denied. Admins only.")
    return payload


def admin_or_vet(payload: dict = Depends(get_current_user)) -> dict:
    if (payload.get("role") or "").upper() not in ("ADMIN", "VETERINARIAN"):
        raise HTTPException(status_code=403, detail="Access denied. Admins and Veterinarians only.")
    return payload


def admin_vet_caretaker(payload: dict = Depends(get_current_user)) -> dict:
    if (payload.get("role") or "").upper() not in ("ADMIN", "VETERINARIAN", "CARETAKER"):
        raise HTTPException(status_code=403, detail="Access denied.")
    return payload


def admin_or_caretaker(payload: dict = Depends(get_current_user)) -> dict:
    if (payload.get("role") or "").upper() not in ("ADMIN", "CARETAKER"):
        raise HTTPException(status_code=403, detail="Access denied. Admins and Caretakers only.")
    return payload
