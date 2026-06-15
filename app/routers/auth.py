from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

class ForgotPasswordBody(BaseModel):
    email: str

@router.post("/login", response_model=schemas.TokenResponse)
def login(body: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Accepts { email, password } and returns a JWT access token."""
    user = db.query(models.User).filter(models.User.email == body.email).first()

    if not user or not auth.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact your administrator.",
        )

    token = auth.create_access_token({"sub": user.email, "role": user.role})

    return schemas.TokenResponse(
        access_token=token,
        user_email=user.email,
        role=user.role,
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        phone=user.phone or "",
    )

@router.get("/me", response_model=schemas.UserOut)
def get_current_user(token: str, db: Session = Depends(get_db)):
    """Verify a JWT and return the logged-in user's info."""
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    user = db.query(models.User).filter(models.User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user

@router.post("/forgot-password")
async def forgot_password(request: Request, db: Session = Depends(get_db)):
    """Safe endpoint that dynamically catches JSON payloads to avoid parsing crash errors."""
    try:
        data = await request.json()
        input_email = data.get("email", "").strip()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data payload template format received."
        )

    if not input_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide your registered officer email address."
        )

    user = db.query(models.User).filter(models.User.email == input_email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This email address is not registered in our system."
        )

    return {"status": "success", "message": "Account verified."}