from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    dep_name = Column(String, nullable=False)
    # salary = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # positions = relationship("Position", back_populates="department")
    positions = relationship("Position", back_populates="department")  

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    position_name = Column(String, nullable=False)
    dep_id = Column(Integer, ForeignKey("departments.id"))
  
    department = relationship("Department", back_populates="positions")  
    employees = relationship("Employee", back_populates="position")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    dob = Column(Date)
    hire_at = Column(Date)
    salary = Column(Integer)
    position_id = Column(Integer, ForeignKey("positions.id"))
    # dep_id = Column(Integer, ForeignKey("departments.id"))
    is_active = Column(Boolean, default=True)
    is_login = Column(Boolean, default=False)
    position = relationship("Position", back_populates="employees")

    # department = relationship("Department")
    # attendances = relationship("Attendance", back_populates="employee")

class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, ForeignKey("employees.id"))
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    status = Column(String)
    # employee = relationship("Employee", back_populates="attendances")

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=True)

