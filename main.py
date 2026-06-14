from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional
from app.database import engine, SessionLocal
from app import models
from app.routers import auth as auth_router
from app.auth import hash_password, verify_password, decode_token

models.Base.metadata.create_all(bind=engine)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class CreateUserRequest(BaseModel):
    email: str
    name: str
    password: str
    role: str = "ADMIN"


class UpdateUserRequest(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated. Please log in.")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    return payload


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter(
            models.User.email == "admin@pcst.com"
        ).first()

        if not admin:
            admin = models.User(
                email="admin@pcst.com",
                password=hash_password("admin123"),
                first_name="Son",
                last_name="Gohan",
                role="ADMIN",
            )
            db.add(admin)
            db.commit()
            print("✅ Default admin seeded: admin@pcst.com / admin123")
        else:
            print("ℹ️ Admin already exists")

    finally:
        db.close()

    yield

    print("🔴 App shutting down")


app = FastAPI(
    title="TailTrack API",
    description="Animal Tracking & Registration — Santa Maria, Pangasinan",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://limegreen-grouse-963064.hostingersite.com"],
    allow_origin_regex=r"https://.*\.hostingersite\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)


@app.post("/changepass")
def post_change_password(
    data: ChangePasswordRequest,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated. Please log in.")

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")

    logged_in_email = payload.get("sub")

    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == logged_in_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        if not verify_password(data.current_password, user.password):
            raise HTTPException(status_code=400, detail="Current password is incorrect.")
        user.password = hash_password(data.new_password)
        db.commit()
        return {"message": "Password updated successfully."}
    finally:
        db.close()


@app.get("/auth/users")
def list_users(payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        return [
            {
                "id": u.id,
                "email": u.email,
                "name": f"{u.first_name or ''} {u.last_name or ''}".strip(),
                "role": u.role,
            }
            for u in users
        ]
    finally:
        db.close()


@app.post("/auth/register", status_code=201)
def register_user(data: CreateUserRequest, payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="A user with this email already exists.")

        parts = data.name.strip().split(" ", 1)
        first = parts[0]
        last  = parts[1] if len(parts) > 1 else ""

        new_user = models.User(
            email=data.email,
            password=hash_password(data.password),
            first_name=first,
            last_name=last,
            role=data.role.upper(),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "id": new_user.id,
            "email": new_user.email,
            "name": f"{new_user.first_name} {new_user.last_name}".strip(),
            "role": new_user.role,
        }
    finally:
        db.close()


@app.put("/auth/users/{user_id}")
def update_user(user_id: int, data: UpdateUserRequest, payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        if data.email:
            conflict = db.query(models.User).filter(
                models.User.email == data.email,
                models.User.id != user_id
            ).first()
            if conflict:
                raise HTTPException(status_code=400, detail="Email already in use.")
            user.email = data.email

        if data.name:
            parts = data.name.strip().split(" ", 1)
            user.first_name = parts[0]
            user.last_name  = parts[1] if len(parts) > 1 else ""

        if data.password:
            user.password = hash_password(data.password)

        if data.role:
            user.role = data.role.upper()

        db.commit()
        db.refresh(user)

        return {
            "id": user.id,
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}".strip(),
            "role": user.role,
        }
    finally:
        db.close()


@app.delete("/auth/users/{user_id}")
def delete_user(user_id: int, payload: dict = Depends(get_current_user)):
    logged_in_email = payload.get("sub")

    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        if user.email == logged_in_email:
            raise HTTPException(status_code=400, detail="You cannot delete your own account.")

        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully."}
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok", "app": "TailTrack API 🐾"}
