# # from fastapi import APIRouter, Depends, HTTPException
# # from sqlalchemy.orm import Session
# # from config.db import get_db
# # from models.user import Admin
# # from schemas.user import AdminCreate, Admin as AdminSchema
# # # from auth.jwt_handler import get_password_hash
# # from passlib.hash import bcrypt
# # from auth.jwt_bearar import JWTBearer


# # router = APIRouter(prefix="/admins", tags=["Admins"])

# # @router.post("/", response_model=AdminSchema)
# # def create_admin(ad: AdminCreate, db: Session = Depends(get_db)):
# #     existing = db.query(Admin).filter(Admin.email == ad.email).first()
# #     if existing:
# #         raise HTTPException(status_code=400, detail="Email already registered")
# #     hashed_pw =  bcrypt.hash(ad.password)
# #     db_ad = Admin(email=ad.email, password=hashed_pw, is_admin=ad.is_admin)
# #     db.add(db_ad)
# #     db.commit()
# #     db.refresh(db_ad)
# #     return db_ad

# # # @router.get("/", response_model=AdminSchema,dependencies=[Depends(JWTBearer())])
# # # def list_admins(db: Session = Depends(get_db)):
# # #     return db.query(Admin).all()
# # @router.get("/", dependencies=[Depends(JWTBearer())])
# # def list_admins():
# #     return {"message": "You are logged in and can view your profile!"}
# # @router.delete("/{admin_id}")
# # def delete_admin(admin_id: int, db: Session = Depends(get_db)):
# #     db_ad = db.query(Admin).filter(Admin.id == admin_id).first()
# #     if not db_ad:
# #         raise HTTPException(status_code=404, detail="Admin not found")
# #     db.delete(db_ad)
# #     db.commit()
# #     return {"detail": f"Admin {admin_id} deleted successfully"}
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from config.db import get_db
# from models.user import Admin
# from schemas.user import AdminCreate, Admin as AdminSchema, LoginBase, Token
# from passlib.hash import bcrypt
# from datetime import timedelta
# from auth.jwt_bearar import JWTBearer
# from auth.jwt_handler import create_access_token

# router = APIRouter(prefix="/admins", tags=["Admins"])

# # -----------------------------
# # Create Admin (Only one allowed)
# # -----------------------------
# @router.post("/", response_model=AdminSchema)
# def create_admin(ad: AdminCreate, db: Session = Depends(get_db)):
#     existing = db.query(Admin).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Only one admin account is allowed")
    
#     hashed_pw = bcrypt.hash(ad.password)
#     db_ad = Admin(email=ad.email, password=hashed_pw, is_admin=ad.is_admin)
#     db.add(db_ad)
#     db.commit()
#     db.refresh(db_ad)
#     return db_ad

# # -----------------------------
# # Admin Login
# # -----------------------------
# @router.post("/login", response_model=Token)
# def login_admin(ad: LoginBase, db: Session = Depends(get_db)):
#     admin = db.query(Admin).filter(Admin.email == ad.email).first()
#     if not admin:
#         raise HTTPException(status_code=400, detail="Admin not found")
#     if not bcrypt.verify(ad.password, admin.password):
#         raise HTTPException(status_code=400, detail="Invalid password")

    
#     token_data = {"sub": admin.email, "admin_id": admin.id}
#     token = create_access_token(token_data)
#     return {"access_token": token, "token_type": "bearer"}

# # -----------------------------
# # Protected Admin Profile
# # -----------------------------
# @router.get("/profile", dependencies=[Depends(JWTBearer())])
# def admin_profile():
#     return {"message": "You are logged in and can view your profile!"}

# # -----------------------------
# # Delete Admin
# # -----------------------------
# @router.delete("/{admin_id}", dependencies=[Depends(JWTBearer())])
# def delete_admin(admin_id: int, db: Session = Depends(get_db)):
#     db_ad = db.query(Admin).filter(Admin.id == admin_id).first()
#     if not db_ad:
#         raise HTTPException(status_code=404, detail="Admin not found")
#     db.delete(db_ad)
#     db.commit()
#     return {"detail": f"Admin {admin_id} deleted successfully"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from models.user import Admin
from schemas.user import AdminCreate, LoginBase, Token
from passlib.hash import bcrypt
from auth.jwt_handler import create_access_token
from auth.jwt_bearar import JWTBearer
from schemas.common import APIResponse

router = APIRouter(prefix="/admins", tags=["Admins"])

# Create Admin (only once)
@router.post("/", response_model=APIResponse)
def create_admin(ad: AdminCreate, db: Session = Depends(get_db)):
    existing = db.query(Admin).first()
    if existing:
        # raise HTTPException(status_code=400, detail="Admin already exists")
        return {"success": False, "message": "Admin already exists", "data": None}
    hashed_pw = bcrypt.hash(ad.password)
    db_ad = Admin(email=ad.email, password=hashed_pw, is_admin=ad.is_admin)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    # return db_ad
    return {"success": True, "message": "Admin created successfully", "data": {"id": db_ad.id, "email": db_ad.email}}

# Admin login
@router.post("/login", response_model=APIResponse)
def login_admin(ad: LoginBase, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == ad.email).first()
    if not admin or not bcrypt.verify(ad.password, admin.password):
        # raise HTTPException(status_code=400, detail="Invalid credentials")
        return {
            "success": False,
            "message": "Invalid email or password",
            "access_token": None,
            "token_type": None
        }
    token_data = {"sub": admin.email, "admin_id": admin.id}
    token = create_access_token(token_data)
    # return {"access_token": token, "token_type": "bearer" ,"message":"Admin sucessfully login"}
    return {
        "success": True,
        "message": "Admin successfully logged in",
        "data": {
            "access_token": token,
            "token_type": "bearer"
        }   }
@router.get("/ adminprofile", dependencies=[Depends(JWTBearer())])
def admin_profile():
    return {
        "success": True,
        "message": "You are logged in and can view your profile!",
        "data": None
    }
