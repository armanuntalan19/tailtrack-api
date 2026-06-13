from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_email: str
    role: str
    first_name: str
    last_name: str


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str | None
    last_name: str | None
    role: str
    is_active: bool

    class Config:
        from_attributes = True
