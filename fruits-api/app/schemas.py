from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class NutritionalInfoBase(BaseModel):
    calories: int
    carbohydrates: float
    protein: float
    fat: float
    fiber: float
    vitamins: str

class NutritionalInfo(NutritionalInfoBase):
    id: int
    fruit_id: int

    class Config:
        from_attributes = True

class SupplierBase(BaseModel):
    name: str
    country: str
    contact_email: str
    rating: float

class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True

class FruitBase(BaseModel):
    name: str
    color: str
    taste: str
    origin_country: str
    price_per_kg: float

class Fruit(FruitBase):
    id: int
    created_at: datetime
    updated_at: datetime
    nutritional_info: Optional[NutritionalInfo] = None
    suppliers: List[Supplier] = []

    class Config:
        from_attributes = True

class FruitComplete(Fruit):
    nutritional_info: NutritionalInfo
    suppliers: List[Supplier] 