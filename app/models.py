from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, index=True, nullable=False)
    password   = Column(String, nullable=False)
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    phone      = Column(String, default="")
    role       = Column(String, default="officer")
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Owner(Base):
    __tablename__ = "owners"

    id        = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone     = Column(String, nullable=False)
    email     = Column(String, default="")
    sitio     = Column(String, default="")
    street    = Column(String, default="")
    landmarks = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    animals = relationship("Animal", back_populates="owner")


class Animal(Base):
    __tablename__ = "animals"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String, nullable=False)
    type            = Column(String, default="dog")
    breed           = Column(String, default="")
    sex             = Column(String, default="Male")
    birthdate       = Column(String, default="")
    color           = Column(String, default="")
    qr_code         = Column(String, default="")
    health_status   = Column(String, default="unknown")
    ownership       = Column(String, default="owned")
    owner_id        = Column(Integer, ForeignKey("owners.id"), nullable=True)
    owner_name      = Column(String, default="")
    owner_contact   = Column(String, default="")
    remarks         = Column(Text, default="")
    image           = Column(Text, default="")
    registered_date = Column(String, default="")
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    owner        = relationship("Owner", back_populates="animals")
    vaccinations = relationship("Vaccination", back_populates="animal")


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id        = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=True)
    name      = Column(String, nullable=False)
    type      = Column(String, default="dog")
    vaccine   = Column(String, default="Anti-Rabies")
    category  = Column(String, default="rabies")
    lot       = Column(String, default="")
    date      = Column(String, nullable=False)
    admin     = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    animal = relationship("Animal", back_populates="vaccinations")


class LostFoundReport(Base):
    __tablename__ = "lost_found_reports"

    id          = Column(Integer, primary_key=True, index=True)
    animal_name = Column(String, nullable=False)
    animal_type = Column(String, default="Dog")
    breed       = Column(String, default="")
    status      = Column(String, default="lost")
    location    = Column(String, nullable=False)
    time_lost   = Column(String, default="")
    description = Column(Text, default="")
    contact     = Column(String, nullable=False)
    date        = Column(String, default="")
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
