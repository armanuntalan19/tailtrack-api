from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func
from app.database import SessionLocal
from app import models, schemas
from app.deps import get_current_user, admin_only, admin_or_caretaker

router = APIRouter(prefix="/lost-found", tags=["lost-and-found"])


def sync_animal_health(db, report):
    animal = None
    if report.animal_id:
        animal = db.query(models.Animal).filter(models.Animal.id == report.animal_id).first()
    if not animal and report.animal_name:
        animal = db.query(models.Animal).filter(
            func.lower(models.Animal.animal_name) == report.animal_name.strip().lower()
        ).first()
    if animal:
        animal.health_status = "missing" if report.status == "lost" else "safe"
        db.commit()


@router.get("", response_model=list[schemas.LostFoundOut])
def list_reports(payload: dict = Depends(get_current_user)):
    # All roles: view
    db = SessionLocal()
    try:
        return db.query(models.LostFoundReport).order_by(models.LostFoundReport.id.desc()).all()
    finally:
        db.close()


@router.get("/{report_id}", response_model=schemas.LostFoundOut)
def get_report(report_id: int, payload: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        report = db.query(models.LostFoundReport).filter(models.LostFoundReport.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found.")
        return report
    finally:
        db.close()


@router.post("", response_model=schemas.LostFoundOut, status_code=201)
def create_report(data: schemas.LostFoundCreate, payload: dict = Depends(admin_or_caretaker)):
    # Admin + Caretaker: add reports. Vet/Viewer: view only.
    db = SessionLocal()
    try:
        report = models.LostFoundReport(**data.model_dump())
        db.add(report)
        db.commit()
        db.refresh(report)
        sync_animal_health(db, report)
        return report
    finally:
        db.close()


@router.put("/{report_id}", response_model=schemas.LostFoundOut)
def update_report(report_id: int, data: schemas.LostFoundUpdate, payload: dict = Depends(admin_only)):
    # Admin only: edit/resolve
    db = SessionLocal()
    try:
        report = db.query(models.LostFoundReport).filter(models.LostFoundReport.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found.")
        updates = data.dict(exclude_unset=True)
        for field, value in updates.items():
            setattr(report, field, value)
        db.commit()
        db.refresh(report)
        if "status" in updates or "animal_id" in updates:
            sync_animal_health(db, report)
        return report
    finally:
        db.close()


@router.delete("/{report_id}")
def delete_report(report_id: int, payload: dict = Depends(admin_only)):
    # Admin only: delete
    db = SessionLocal()
    try:
        report = db.query(models.LostFoundReport).filter(models.LostFoundReport.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found.")
        db.delete(report)
        db.commit()
        return {"message": "Report deleted successfully."}
    finally:
        db.close()