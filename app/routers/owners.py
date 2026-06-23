from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app import models, schemas
from app.deps import admin_or_vet, admin_only

router = APIRouter(prefix="/owners", tags=["owners"])


@router.get("", response_model=list[schemas.OwnerOut])
def list_owners(payload: dict = Depends(admin_or_vet)):
    # Admin + Vet: view
    db = SessionLocal()
    try:
        return db.query(models.Owner).order_by(models.Owner.id.desc()).all()
    finally:
        db.close()


@router.get("/{owner_id}", response_model=schemas.OwnerOut)
def get_owner(owner_id: int, payload: dict = Depends(admin_or_vet)):
    db = SessionLocal()
    try:
        owner = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found.")
        return owner
    finally:
        db.close()


@router.post("", response_model=schemas.OwnerOut, status_code=201)
def create_owner(data: schemas.OwnerCreate, payload: dict = Depends(admin_only)):
    # Admin only: add/edit/delete
    db = SessionLocal()
    try:
        owner = models.Owner(**data.model_dump())
        db.add(owner)
        db.commit()
        db.refresh(owner)
        return owner
    finally:
        db.close()


@router.put("/{owner_id}", response_model=schemas.OwnerOut)
def update_owner(owner_id: int, data: schemas.OwnerUpdate, payload: dict = Depends(admin_only)):
    db = SessionLocal()
    try:
        owner = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found.")
        for field, value in data.dict(exclude_unset=True).items():
            setattr(owner, field, value)
        db.commit()
        db.refresh(owner)
        return owner
    finally:
        db.close()


@router.delete("/{owner_id}")
def delete_owner(owner_id: int, payload: dict = Depends(admin_only)):
    db = SessionLocal()
    try:
        owner = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found.")
        db.delete(owner)
        db.commit()
        return {"message": "Owner deleted successfully."}
    finally:
        db.close()
