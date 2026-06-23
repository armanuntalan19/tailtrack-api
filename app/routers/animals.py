from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app import models, schemas
from app.deps import get_current_user, admin_or_vet, admin_only

router = APIRouter(prefix="/animals", tags=["animals"])


@router.get("/public/{animal_id}")
def get_animal_public(animal_id: int):
    """Public — no auth. Used by QR code scans."""
    db = SessionLocal()
    try:
        animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found.")
        return {
            "id": animal.id, "animal_name": animal.animal_name,
            "species": animal.species, "breed": animal.breed,
            "sex": animal.sex,
            "birthdate": str(animal.birthdate) if animal.birthdate else None,
            "color_markings": animal.color_markings,
            "health_status": animal.health_status,
            "ownership": animal.ownership,
            "owner_name": animal.owner_name,
            "owner_contact": animal.owner_contact,
            "remarks": animal.remarks, "image": animal.image,
        }
    finally:
        db.close()


@router.get("", response_model=list[schemas.AnimalOut])
def list_animals(payload: dict = Depends(get_current_user)):
    # All roles: view
    db = SessionLocal()
    try:
        return db.query(models.Animal).order_by(models.Animal.id.desc()).all()
    finally:
        db.close()


@router.get("/{animal_id}", response_model=schemas.AnimalOut)
def get_animal(animal_id: int, payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found.")
        return animal
    finally:
        db.close()


@router.post("", response_model=schemas.AnimalOut, status_code=201)
def create_animal(data: schemas.AnimalCreate, payload: dict = Depends(admin_or_vet)):
    # Admin + Vet: add
    db = SessionLocal()
    try:
        if data.owner_id is not None:
            owner = db.query(models.Owner).filter(models.Owner.id == data.owner_id).first()
            if not owner:
                raise HTTPException(status_code=400, detail="Owner not found.")
        animal = models.Animal(**data.model_dump())
        db.add(animal)
        db.commit()
        db.refresh(animal)
        return animal
    finally:
        db.close()


@router.put("/{animal_id}", response_model=schemas.AnimalOut)
def update_animal(animal_id: int, data: schemas.AnimalUpdate, payload: dict = Depends(admin_or_vet)):
    # Admin + Vet: edit
    db = SessionLocal()
    try:
        animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found.")
        updates = data.dict(exclude_unset=True)
        if "owner_id" in updates and updates["owner_id"] is not None:
            owner = db.query(models.Owner).filter(models.Owner.id == updates["owner_id"]).first()
            if not owner:
                raise HTTPException(status_code=400, detail="Owner not found.")
        for field, value in updates.items():
            setattr(animal, field, value)
        db.commit()
        db.refresh(animal)
        return animal
    finally:
        db.close()


@router.delete("/{animal_id}")
def delete_animal(animal_id: int, payload: dict = Depends(admin_only)):
    # Admin only: delete
    db = SessionLocal()
    try:
        animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found.")
        db.delete(animal)
        db.commit()
        return {"message": "Animal deleted successfully."}
    finally:
        db.close()
