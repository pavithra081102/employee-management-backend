from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from config.db import get_db
from models.user import Attendance, Employee
from schemas.user import AttendanceCreate, Attendance as AttendanceSchema

router = APIRouter(prefix="/attendances", tags=["Attendances"])

@router.post("/", response_model=AttendanceSchema)
def create_attendance(at: AttendanceCreate, db: Session = Depends(get_db)):
    # ensure employee exists
    emp = db.query(Employee).filter(Employee.id == at.emp_id).first()
    if not emp:
        raise HTTPException(status_code=400, detail="Employee does not exist")
    db_at = Attendance(
        emp_id=at.emp_id,
        check_in=at.check_in,
        check_out=at.check_out,
        status=at.status
    )
    db.add(db_at)
    db.commit()
    db.refresh(db_at)
    return db_at

@router.get("/", response_model=list[AttendanceSchema])
def list_attendances(db: Session = Depends(get_db)):
    return db.query(Attendance).all()

@router.put("/{at_id}", response_model=AttendanceSchema)
def update_attendance(at_id: int, at: AttendanceCreate, db: Session = Depends(get_db)):
    db_at = db.query(Attendance).filter(Attendance.id == at_id).first()
    if not db_at:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    # optionally check employee
    emp = db.query(Employee).filter(Employee.id == at.emp_id).first()
    if not emp:
        raise HTTPException(status_code=400, detail="Employee does not exist")
    db_at.emp_id = at.emp_id
    db_at.check_in = at.check_in
    db_at.check_out = at.check_out
    db_at.status = at.status
    db.commit()
    db.refresh(db_at)
    return db_at

@router.delete("/{at_id}")
def delete_attendance(at_id: int, db: Session = Depends(get_db)):
    db_at = db.query(Attendance).filter(Attendance.id == at_id).first()
    if not db_at:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    db.delete(db_at)
    db.commit()
    return {"detail": f"Attendance record {at_id} deleted successfully"}
