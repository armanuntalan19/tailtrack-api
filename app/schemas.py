from pydantic import BaseModel
from datetime import date as date_type, datetime as datetime_type


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
    phone: str


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str | None
    last_name: str | None
    phone_number: str | None
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class OwnerBase(BaseModel):
    full_name: str
    phone_number: str
    email: str = ""
    sitio: str = ""
    residency_street: str = ""
    landmarks: str = ""


class OwnerCreate(OwnerBase):
    pass


class OwnerUpdate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    sitio: str | None = None
    residency_street: str | None = None
    landmarks: str | None = None


class OwnerOut(OwnerBase):
    id: int

    class Config:
        from_attributes = True


class AnimalBase(BaseModel):
    animal_name: str
    species: str = "dog"
    breed: str | None = ""
    sex: str | None = "Male"
    birthdate: date_type | None = None
    color_markings: str | None = ""
    qr_code: str | None = ""
    health_status: str | None = "unknown"
    ownership: str | None = "owned"
    owner_id: int | None = None
    owner_name: str | None = ""
    owner_contact: str | None = ""
    remarks: str | None = ""
    image: str | None = ""


class AnimalCreate(AnimalBase):
    pass


class AnimalUpdate(BaseModel):
    animal_name: str | None = None
    species: str | None = None
    breed: str | None = None
    sex: str | None = None
    birthdate: date_type | None = None
    color_markings: str | None = None
    qr_code: str | None = None
    health_status: str | None = None
    ownership: str | None = None
    owner_id: int | None = None
    owner_name: str | None = None
    owner_contact: str | None = None
    remarks: str | None = None
    image: str | None = None


class AnimalOut(AnimalBase):
    id: int

    class Config:
        from_attributes = True


class VaccinationBase(BaseModel):
    animal_id: int | None = None
    animal_name: str
    animel_type: str | None = "dog"
    vaccine: str | None = "Anti-Rabies"
    category: str | None = "rabies"
    lot_number: str | None = ""
    date: date_type
    administered_by: str


class VaccinationCreate(VaccinationBase):
    pass


class VaccinationUpdate(BaseModel):
    animal_id: int | None = None
    animal_name: str | None = None
    animel_type: str | None = None
    vaccine: str | None = None
    category: str | None = None
    lot_number: str | None = None
    date: date_type | None = None
    administered_by: str | None = None


class VaccinationOut(VaccinationBase):
    id: int

    class Config:
        from_attributes = True


class LostFoundBase(BaseModel):
    animal_name: str
    animal_type: str | None = "Dog"
    breed: str | None = ""
    status: str | None = "lost"
    sitio_area: str
    time_lost: datetime_type | None = None
    description: str | None = ""
    contact_person: str


class LostFoundCreate(LostFoundBase):
    pass


class LostFoundUpdate(BaseModel):
    animal_name: str | None = None
    animal_type: str | None = None
    breed: str | None = None
    status: str | None = None
    sitio_area: str | None = None
    time_lost: datetime_type | None = None
    description: str | None = None
    contact_person: str | None = None


class LostFoundOut(LostFoundBase):
    id: int

    class Config:
        from_attributes = True
