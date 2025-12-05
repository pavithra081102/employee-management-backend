from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import date, datetime


# Department
class DepartmentBase(BaseModel):
    dep_name: str
    # salary: int
    is_active: Optional[bool] = True

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)

# Position
class PositionBase(BaseModel):
    position_name: str
    dep_id: int

class PositionCreate(PositionBase):
    pass

class Position(PositionBase):
    id: int
    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)

# Employee
class PositionSchema(BaseModel):
    id: int
    position_name: str
    model_config = ConfigDict(from_attributes=True)
class EmployeeBase(BaseModel):
    name: str
    email: str
    dob: date
    hire_at: date
    salary:float
    position_id: int
    is_active: Optional[bool] = True
    
    # dep_id: int

class EmployeeCreate(EmployeeBase):
    password: str

    
    # nested

    
class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    dob: Optional[date] = None
    hire_at: Optional[date] = None
    salary: Optional[float] = None
    position_id: Optional[int] = None
    is_active:Optional[bool]=None

class Employee(EmployeeBase):
    id: int
    is_login: bool
    is_active:bool
 
    position: Optional[PositionSchema] = None   
    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)

# Attendance
class AttendanceBase(BaseModel):
    emp_id: int
    check_in: datetime
    check_out: Optional[datetime]
    status: str

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)

# Admin
class AdminBase(BaseModel):
    email: str
    password: str
    is_admin: Optional[bool] = True

class AdminCreate(AdminBase):
    pass

class Admin(AdminBase):
    id: int
    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)

# # Login
class LoginBase(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
