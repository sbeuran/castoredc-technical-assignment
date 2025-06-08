from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....database import get_db
from ....models import Fruit as FruitModel
from ....schemas import FruitComplete

router = APIRouter()

@router.get("/get_all_data", response_model=List[FruitComplete], tags=["data"])
async def get_all_data(db: Session = Depends(get_db)):
    """
    Get all fruits with their complete information including nutritional data and suppliers.
    """
    fruits = db.query(FruitModel).all()
    if not fruits:
        raise HTTPException(status_code=404, detail="No data found")
    return fruits 