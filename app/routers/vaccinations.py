from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app import models, schemas
from app.deps import get_current_user

router = APIRouter(prefix="/vaccinations", tags=["vaccinations"])


@router.get("", response_model=list[schemas.VaccinationOut])
def list_vaccinations(payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        return db.query(models.Vaccination).order_by(models.Vaccination.id.desc()).all()
    finally:
        db.close()


@router.get("/{record_id}", response_model=schemas.VaccinationOut)
def get_vaccination(record_id: int, payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        record = db.query(models.Vaccination).filter(models.Vaccination.id == record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Vaccination record not found.")
        return record
    finally:
        db.close()


@router.post("", response_model=schemas.VaccinationOut, status_code=201)
def create_vaccination(data: schemas.VaccinationCreate, payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        if data.animal_id is not None:
            animal = db.query(models.Animal).filter(models.Animal.id == data.animal_id).first()
            if not animal:
                raise HTTPException(status_code=400, detail="Animal not found.")

        record = models.Vaccination(**data.model_dump())
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()


@router.put("/{record_id}", response_model=schemas.VaccinationOut)
def update_vaccination(record_id: int, data: schemas.VaccinationUpdate, payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        record = db.query(models.Vaccination).filter(models.Vaccination.id == record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Vaccination record not found.")

        updates = data.dict(exclude_unset=True)

        if "animal_id" in updates and updates["animal_id"] is not None:
            animal = db.query(models.Animal).filter(models.Animal.id == updates["animal_id"]).first()
            if not animal:
                raise HTTPException(status_code=400, detail="Animal not found.")

        for field, value in updates.items():
            setattr(record, field, value)

        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()


@router.delete("/{record_id}")
def delete_vaccination(record_id: int, payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        record = db.query(models.Vaccination).filter(models.Vaccination.id == record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Vaccination record not found.")

        db.delete(record)
        db.commit()
        return {"message": "Vaccination record deleted successfully."}
    finally:
        db.close()
