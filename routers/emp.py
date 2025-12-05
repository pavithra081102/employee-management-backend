# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError
# from models.user import Employee, Position
# from schemas.user import EmployeeCreate, EmployeeUpdate
# from schemas.user import Employee as EmployeeSchema, Position as PositionSchema
# from schemas.common import APIResponse
# from config.db import get_db
# from passlib.hash import bcrypt
# from auth.jwt_bearar import JWTBearer

# router = APIRouter(prefix="/employees", tags=["Employees"])


# # -----------------------------
# # Create Employee
# # -----------------------------
# @router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
# def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
#     # Check position exists
#     position = db.query(Position).filter(Position.id == emp.position_id).first()
#     if not position:
#         raise HTTPException(status_code=400, detail="Position does not exist")

#     hashed_pw = bcrypt.hash(emp.password)
#     db_emp = Employee(
#         name=emp.name,
#         email=emp.email,
#         password=hashed_pw,
#         dob=emp.dob,
#         hire_at=emp.hire_at,
#         salary=emp.salary,
#         position_id=emp.position_id,
#         is_active=emp.is_active,
#         is_login=False
#     )

#     try:
#         db.add(db_emp)
#         db.commit()
#         db.refresh(db_emp)
        
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="Invalid data or foreign key violation")

#     emp_data = EmployeeSchema.from_orm(db_emp)
#     return {"message": "Employee created successfully", "data": emp_data}


# # -----------------------------
# # List Employees
# # -----------------------------
# @router.get("/", response_model=list[EmployeeSchema], status_code=status.HTTP_200_OK)
# def list_employees(db: Session = Depends(get_db)):
#     employees = db.query(Employee).all()
#     return [
#         EmployeeSchema(
#             id=emp.id,
#             name=emp.name,
#             email=emp.email,
#             dob=emp.dob,
#             hire_at=emp.hire_at,
#             salary=emp.salary,
#             position_id=emp.position_id,
#             is_login=emp.is_login,
#             is_active=emp.is_active,
#             position=PositionSchema.from_orm(emp.position) if emp.position else None
#         )
#         for emp in employees
#     ]


# # -----------------------------
# # Update Employee
# # -----------------------------
# @router.put("/{emp_id}", response_model=APIResponse, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
# def update_employee(emp_id: int, emp: EmployeeUpdate, db: Session = Depends(get_db)):
#     db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
#     if not db_emp:
#         raise HTTPException(status_code=404, detail="Employee not found")

#     update_data = emp.dict(exclude_unset=True)

#     # Check if position_id is being updated
#     if "position_id" in update_data:
#         position = db.query(Position).filter(Position.id == update_data["position_id"]).first()
#         if not position:
#             raise HTTPException(status_code=400, detail="Position does not exist")

#     for key, value in update_data.items():
#         if key == "password":
#             setattr(db_emp, key, bcrypt.hash(value))
#         else:
#             setattr(db_emp, key, value)

#     try:
#         db.commit()
#         db.refresh(db_emp)
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="Invalid data or foreign key violation")

#     emp_data = EmployeeSchema.from_orm(db_emp)
#     return {"message": "Employee updated successfully", "data": emp_data}


# # -----------------------------
# # Delete Employee
# # -----------------------------
# @router.delete("/{emp_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
# def delete_employee(emp_id: int, db: Session = Depends(get_db)):
#     db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
#     if not db_emp:
#         raise HTTPException(status_code=404, detail="Employee not found")

#     db.delete(db_emp)
#     db.commit()
#     return {"message": f"Employee {emp_id} deleted successfully", "data": None}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import Employee, Position
from schemas.user import EmployeeCreate, EmployeeUpdate
from schemas.user import Employee as EmployeeSchema, Position as PositionSchema
from schemas.common import APIResponse
from config.db import get_db
from passlib.hash import bcrypt
from auth.jwt_bearar import JWTBearer

router = APIRouter(prefix="/employees", tags=["Employees"])

# -----------------------------
# Create Employee
# -----------------------------
@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        # Check position exists
        position = db.query(Position).filter(Position.id == emp.position_id).first()
        if not position:
            return {"success": False, "message": "Position does not exist", "data": None}

        hashed_pw = bcrypt.hash(emp.password)
        db_emp = Employee(
            name=emp.name,
            email=emp.email,
            password=hashed_pw,
            dob=emp.dob,
            hire_at=emp.hire_at,
            salary=emp.salary,
            position_id=emp.position_id,
            is_active=emp.is_active,
            is_login=False
        )

        db.add(db_emp)
        db.commit()
        db.refresh(db_emp)

        emp_data = EmployeeSchema.from_orm(db_emp)
        return {"success": True, "message": "Employee created successfully", "data": emp_data}

    except IntegrityError:
        db.rollback()
        return {"success": False, "message": "Invalid data or foreign key violation", "data": None}
    except Exception as e:
        return {"success": False, "message": str(e), "data": None}


# -----------------------------
# List Employees
# -----------------------------
# @router.get("/", response_model=list[EmployeeSchema],dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
# def list_employees(db: Session = Depends(get_db)):
#     employees = db.query(Employee).all()
#     return [
#         EmployeeSchema(
#             id=emp.id,
#             name=emp.name,
#             email=emp.email,
#             dob=emp.dob,
#             hire_at=emp.hire_at,
#             salary=emp.salary,
#             position_id=emp.position_id,
#             is_login=emp.is_login,
#             is_active=emp.is_active,
#             position=PositionSchema.from_orm(emp.position) if emp.position else None
#         )
#         for emp in employees
#     ]
@router.get("/", status_code=status.HTTP_200_OK)
def list_employees(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    # Total records in DB
    total_records = db.query(Employee).count()
    total_pages = (total_records + limit - 1) // limit  # ceiling division

    # Pagination offset
    skip = (page - 1) * limit

    # Fetch paginated data
    employees = (
        db.query(Employee)
        .offset(skip)
        .limit(limit)
        .all()
    )

    emp_data = [EmployeeSchema.from_orm(emp) for emp in employees]
    return {
        "success": True,
        "message": "Position Created successfully",
        "total_records": total_records,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "next_page": page + 1 if page < total_pages else None,
        "data": emp_data
    }

# -----------------------------
# Update Employee
# -----------------------------
@router.put("/{emp_id}", response_model=APIResponse, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
def update_employee(emp_id: int, emp: EmployeeUpdate, db: Session = Depends(get_db)):
    try:
        db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
        if not db_emp:
            return {"success": False, "message": "Employee not found", "data": None}

        update_data = emp.dict(exclude_unset=True)

        # Check if position_id is being updated
        if "position_id" in update_data:
            position = db.query(Position).filter(Position.id == update_data["position_id"]).first()
            if not position:
                return {"success": False, "message": "Position does not exist", "data": None}

        for key, value in update_data.items():
            if key == "password":
                setattr(db_emp, key, bcrypt.hash(value))
            else:
                setattr(db_emp, key, value)

        db.commit()
        db.refresh(db_emp)
        emp_data = EmployeeSchema.from_orm(db_emp)
        return {"success": True, "message": "Employee updated successfully", "data": emp_data}

    except IntegrityError:
        db.rollback()
        return {"success": False, "message": "Invalid data or foreign key violation", "data": None}
    except Exception as e:
        return {"success": False, "message": str(e), "data": None}


# -----------------------------
# Delete Employee
# -----------------------------
@router.delete("/{emp_id}", response_model=APIResponse, dependencies=[Depends(JWTBearer())],status_code=status.HTTP_200_OK)
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    try:
        db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
        if not db_emp:
            return {"success": False, "message": "Employee not found", "data": None}

        db.delete(db_emp)
        db.commit()
        return {"success": True, "message": f"Employee {emp_id} deleted successfully", "data": None}

    except Exception as e:
        return {"success": False, "message": str(e), "data": None}
