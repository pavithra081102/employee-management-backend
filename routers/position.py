from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from config.db import get_db
from models.user import Position, Department
from schemas.user import PositionCreate, Position as PositionSchema
from schemas.common import APIResponse
from auth.jwt_bearar import JWTBearer

router = APIRouter(prefix="/positions", tags=["Positions"])

@router.post("/", response_model=APIResponse,status_code=status.HTTP_201_CREATED)
def create_position(pos: PositionCreate, db: Session = Depends(get_db)):
    # ensure department exists
    dep = db.query(Department).filter(Department.id == pos.dep_id).first()
    if not dep:
        # raise HTTPException(status_code=400, detail="Department does not exist")
        return{
            "success":False,
            "message":"Department does not exists",
            "data":None
        }
    db_pos = Position(position_name=pos.position_name, dep_id=pos.dep_id)
    db.add(db_pos)
    db.commit()
    db.refresh(db_pos)
    pos_data = PositionSchema.from_orm(db_pos)
    return {
        "success":True,
        "message": "Position created successfully",
        "data": pos_data
    }

# @router.get("/", response_model=list[PositionSchema],dependencies=[Depends(JWTBearer())])
# def list_positions(db: Session = Depends(get_db)):
#     return db.query(Position).all()
@router.get("/", status_code=status.HTTP_200_OK)
def list_positions(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    # Total records in DB
    total_records = db.query(Position).count()
    total_pages = (total_records + limit - 1) // limit  # ceiling division

    # Pagination offset
    skip = (page - 1) * limit

    # Fetch paginated data
    positions = (
        db.query(Position)
        .offset(skip)
        .limit(limit)
        .all()
    )

    pos_data = [PositionSchema.from_orm(pos) for pos in positions]
    return {
        "success": True,
        "message": "Position Created successfully",
        "total_records": total_records,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit,
        "next_page": page + 1 if page < total_pages else None,
        "data": pos_data
    }
@router.put("/{pos_id}", response_model=APIResponse,dependencies=[Depends(JWTBearer())],status_code=status.HTTP_200_OK)
def update_position(pos_id: int, pos: PositionCreate, db: Session = Depends(get_db)):
    db_pos = db.query(Position).filter(Position.id == pos_id).first()
    if not db_pos:
        # raise HTTPException(status_code=404, detail="Position not found")
        return{
            "success":False,
            "message":"Position not found",
            "data":None
        }
    # ensure new department exists
    dep = db.query(Department).filter(Department.id == pos.dep_id).first()
    if not dep:
        # raise HTTPException(status_code=400, detail="Department does not exist")
        return{
            "success":False,
            "message":"Department does not exits",
            "data":None
        }
    db_pos.position_name = pos.position_name
    db_pos.dep_id = pos.dep_id
    db.commit()
    db.refresh(db_pos)
    pos_data = PositionSchema.from_orm(db_pos)
    return {
        "success":True,
        "message": "Position updated successfully",
        "data": pos_data
    }

@router.delete("/{pos_id}",dependencies=[Depends(JWTBearer())])
def delete_position(pos_id: int, db: Session = Depends(get_db)):
    db_pos = db.query(Position).filter(Position.id == pos_id).first()
    if not db_pos:
        # raise HTTPException(status_code=404, detail="Position not found")
        return{
            "success":False,
            "message":"Position not found",
            "data":None
        }
    db.delete(db_pos)
    db.commit()
    # return {"detail": f"Position {pos_id} deleted successfully"}
    return {
        "success": True,
        "message": f"Position {pos_id} deleted successfully",
        "data": None
    }
