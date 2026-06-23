from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app import models, schemas
from app.deps import get_current_user, admin_only, admin_vet_caretaker

router = APIRouter(prefix="/lost-found", tags=["lost-and-found"])


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
def create_report(data: schemas.LostFoundCreate, payload: dict = Depends(admin_vet_caretaker)):
    # Admin + Vet + Caretaker: add reports
    db = SessionLocal()
    try:
        report = models.LostFoundReport(**data.model_dump())
        db.add(report)
        db.commit()
        db.refresh(report)
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
        for field, value in data.dict(exclude_unset=True).items():
            setattr(report, field, value)
        db.commit()
        db.refresh(report)
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
