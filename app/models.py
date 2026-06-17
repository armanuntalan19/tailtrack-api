from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "User_Management"

    id           = Column(Integer, primary_key=True, index=True)
    email        = Column(String, unique=True, index=True, nullable=False)
    password     = Column(String, nullable=False)
    first_name   = Column(String, default="")
    last_name    = Column(String, default="")
    role         = Column(String, default="officer")
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    phone_number = Column(String, default="")


class Owner(Base):
    __tablename__ = "Owners"

    id               = Column(Integer, primary_key=True, index=True)
    full_name        = Column(String, nullable=False)
    phone_number     = Column(String, nullable=False)
    email            = Column(String, default="")
    sitio            = Column(String, default="")
    residency_street = Column(String, default="")
    landmarks        = Column(String, default="")
    created_at       = Column(DateTime(timezone=True), server_default=func.now())

    animals = relationship("Animal", back_populates="owner")


class Animal(Base):
    __tablename__ = "Animal_Registry"

    id              = Column(Integer, primary_key=True, index=True)
    animal_name     = Column(String, nullable=False)
    species         = Column(String, default="dog")
    breed           = Column(String, default="")
    sex             = Column(String, default="Male")
    birthdate       = Column(Date, nullable=True)
    color_markings  = Column(String, default="")
    qr_code         = Column(String, default="")
    health_status   = Column(String, default="unknown")
    ownership       = Column(String, default="owned")
    owner_id        = Column(Integer, ForeignKey("Owners.id"), nullable=True)
    owner_name      = Column(String, default="")
    owner_contact   = Column(String, default="")
    remarks         = Column(Text, default="")
    image           = Column(Text, default="")
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    owner        = relationship("Owner", back_populates="animals")
    vaccinations = relationship("Vaccination", back_populates="animal")


class Vaccination(Base):
    __tablename__ = "Vaccinations"

    id              = Column(Integer, primary_key=True, index=True)
    animal_id       = Column(Integer, ForeignKey("Animal_Registry.id"), nullable=True)
    animal_name     = Column(String, nullable=False)
    animel_type     = Column(String, default="dog")
    vaccine         = Column(String, default="Anti-Rabies")
    category        = Column(String, default="rabies")
    lot_number      = Column(String, default="")
    date            = Column(Date, nullable=False)
    administered_by = Column(String, nullable=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    animal = relationship("Animal", back_populates="vaccinations")


class LostFoundReport(Base):
    __tablename__ = "Lost_Found"

    id              = Column(Integer, primary_key=True, index=True)
    animal_name     = Column(String, nullable=False)
    animal_type     = Column(String, default="Dog")
    breed           = Column(String, default="")
    status          = Column(String, default="lost")
    sitio_area      = Column(String, nullable=False)
    time_lost       = Column(DateTime(timezone=True), nullable=True)
    description     = Column(Text, default="")
    contact_person  = Column(String, nullable=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
