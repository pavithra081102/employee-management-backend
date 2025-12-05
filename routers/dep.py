from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from config.db import get_db
from models.user import Department
from schemas.user import DepartmentCreate, Department as DepartmentSchema
from schemas.common import APIResponse

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=APIResponse,status_code=status.HTTP_201_CREATED)
def create_department(dep: DepartmentCreate, db: Session = Depends(get_db)):
    db_dep = Department(dep_name=dep.dep_name,  is_active=dep.is_active)
    db.add(db_dep)
    db.commit()
    db.refresh(db_dep)
    dep_data = DepartmentSchema.from_orm(db_dep)
    return {
        "success": True,
        "message": "Department created successfully",
        "data": dep_data
    }

# @router.get("/", response_model=list[DepartmentSchema],status_code=status.HTTP_200_OK)
# def list_departments(db: Session = Depends(get_db)):
#     return db.query(Department).all()
@router.get("/", status_code=status.HTTP_200_OK)
def list_departments(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    # Total records in DB
    total_records = db.query(Department).count()
    total_pages = (total_records + limit - 1) // limit  # ceiling division

    # Pagination offset
    skip = (page - 1) * limit

    # Fetch paginated data
    departments = (
        db.query(Department)
        .offset(skip)
        .limit(limit)
        .all()
    )

    dep_data = [DepartmentSchema.from_orm(dep) for dep in departments]

    return {
        "success": True,
        "message": "Departments fetched successfully",
        "total_records": total_records,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "next_page": page + 1 if page < total_pages else None,
        "data": dep_data
    }


@router.put("/{dep_id}", response_model=APIResponse,status_code=status.HTTP_200_OK)
def update_department(dep_id: int, dep: DepartmentCreate, db: Session = Depends(get_db)):
    db_dep = db.query(Department).filter(Department.id == dep_id).first()
    if not db_dep:
        # raise HTTPException(status_code=404, detail="Department not found")
        return{
            "success":False,
            "message":"Department not found",
            "data":None

        }
    db_dep.dep_name = dep.dep_name
    
    db_dep.is_active = dep.is_active
    db.commit()
    db.refresh(db_dep)
    dep_data = DepartmentSchema.from_orm(db_dep)
    return {
        "success": True,
        "message": "Department updated successfully",
        "data": dep_data
    }

@router.delete("/{dep_id}")
def delete_department(dep_id: int, db: Session = Depends(get_db)):
    db_dep = db.query(Department).filter(Department.id == dep_id).first()
    if not db_dep:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_dep)
    db.commit()
    # return {"detail": f"Department {dep_id} deleted successfully"}
    return {
        "success": True,
        "message": f"Department {dep_id} deleted successfully",
        "data": None
    }

