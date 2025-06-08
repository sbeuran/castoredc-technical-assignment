from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Fruit, NutritionalInfo, Supplier, FruitSupplier
from app.schemas import Fruit as FruitSchema, NutritionalInfo as NutritionalInfoSchema, Supplier as SupplierSchema
from pydantic import BaseModel

router = APIRouter()

# Basic fruit model as per requirements
class BasicFruit(BaseModel):
    id: int
    fruit: str
    color: str

class BasicFruitCreate(BaseModel):
    fruit: str
    color: str

# Initialize some data
def init_data(db: Session):
    try:
        # Check if we already have data
        if db.query(Fruit).count() == 0:
            # Add suppliers first
            suppliers_data = [
                {
                    "name": "Fresh Farms",
                    "country": "USA",
                    "contact_email": "contact@freshfarms.com",
                    "rating": 4.5
                },
                {
                    "name": "Global Fruits Co",
                    "country": "Spain",
                    "contact_email": "info@globalfruits.com",
                    "rating": 4.8
                },
                {
                    "name": "Tropical Exports",
                    "country": "Ecuador",
                    "contact_email": "sales@tropicalexports.com",
                    "rating": 4.2
                }
            ]
            
            # Create and store suppliers
            suppliers = {}
            for supplier_data in suppliers_data:
                supplier = Supplier(**supplier_data)
                db.add(supplier)
                db.flush()
                suppliers[supplier.country] = supplier

            # Add fruits with nutritional info
            fruits_data = [
                {
                    "fruit": {
                        "name": "Apple",
                        "color": "Red",
                        "taste": "Sweet",
                        "origin_country": "USA",
                        "price_per_kg": 2.99
                    },
                    "nutrition": {
                        "calories": 52,
                        "carbohydrates": 14,
                        "protein": 0.3,
                        "fat": 0.2,
                        "fiber": 2.4,
                        "vitamins": "A, C"
                    }
                },
                {
                    "fruit": {
                        "name": "Banana",
                        "color": "Yellow",
                        "taste": "Sweet",
                        "origin_country": "Ecuador",
                        "price_per_kg": 1.99
                    },
                    "nutrition": {
                        "calories": 89,
                        "carbohydrates": 23,
                        "protein": 1.1,
                        "fat": 0.3,
                        "fiber": 2.6,
                        "vitamins": "B6, C"
                    }
                },
                {
                    "fruit": {
                        "name": "Orange",
                        "color": "Orange",
                        "taste": "Sweet-Citrus",
                        "origin_country": "Spain",
                        "price_per_kg": 3.49
                    },
                    "nutrition": {
                        "calories": 47,
                        "carbohydrates": 12,
                        "protein": 0.9,
                        "fat": 0.1,
                        "fiber": 2.4,
                        "vitamins": "C"
                    }
                }
            ]

            for data in fruits_data:
                # Create fruit
                fruit = Fruit(**data["fruit"])
                db.add(fruit)
                db.flush()

                # Create nutritional info
                nutrition = NutritionalInfo(fruit_id=fruit.id, **data["nutrition"])
                db.add(nutrition)

                # Link supplier from the same country
                if fruit.origin_country in suppliers:
                    supplier = suppliers[fruit.origin_country]
                    fruit_supplier = FruitSupplier(fruit_id=fruit.id, supplier_id=supplier.id)
                    db.add(fruit_supplier)

            db.commit()
            print("Database initialized with complete data!")
    except Exception as e:
        print(f"Error initializing data: {e}")
        db.rollback()

@router.get("/fruits", response_model=List[BasicFruit])
async def get_fruits(db: Session = Depends(get_db)):
    """
    Get all fruits in basic format as per requirements.
    """
    # Initialize data if needed
    init_data(db)
    
    fruits = db.query(Fruit).all()
    return [{"id": f.id, "fruit": f.name, "color": f.color} for f in fruits]

@router.get("/fruits/{fruit_id}", response_model=BasicFruit)
async def get_fruit(fruit_id: int, db: Session = Depends(get_db)):
    """
    Get a specific fruit by ID in basic format as per requirements.
    """
    fruit = db.query(Fruit).filter(Fruit.id == fruit_id).first()
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return {"id": fruit.id, "fruit": fruit.name, "color": fruit.color}

@router.post("/fruits", response_model=BasicFruit)
async def create_fruit(fruit: BasicFruitCreate, db: Session = Depends(get_db)):
    """
    Create a new fruit using basic format as per requirements.
    """
    db_fruit = Fruit(name=fruit.fruit, color=fruit.color)
    db.add(db_fruit)
    db.commit()
    db.refresh(db_fruit)
    return {"id": db_fruit.id, "fruit": db_fruit.name, "color": db_fruit.color}

@router.get("/get_all_data", response_model=dict)
async def get_all_data(db: Session = Depends(get_db)):
    """
    Get all data from the database including fruits, nutritional info, and suppliers.
    """
    try:
        # Initialize data if needed
        init_data(db)
        
        # Get all fruits with their nutritional info and suppliers
        fruits = db.query(Fruit).all()
        nutritional_info = db.query(NutritionalInfo).all()
        suppliers = db.query(Supplier).all()

        return {
            "fruits": [
                {
                    "id": fruit.id,
                    "name": fruit.name,
                    "color": fruit.color,
                    "taste": fruit.taste,
                    "origin_country": fruit.origin_country,
                    "price_per_kg": float(fruit.price_per_kg),
                    "suppliers": [
                        {
                            "id": supplier.id,
                            "name": supplier.name,
                            "contact_email": supplier.contact_email,
                            "country": supplier.country,
                            "rating": supplier.rating
                        }
                        for supplier in fruit.suppliers
                    ],
                    "nutritional_info": {
                        "id": fruit.nutritional_info.id,
                        "calories": fruit.nutritional_info.calories,
                        "carbohydrates": fruit.nutritional_info.carbohydrates,
                        "protein": fruit.nutritional_info.protein,
                        "fat": fruit.nutritional_info.fat,
                        "fiber": fruit.nutritional_info.fiber,
                        "vitamins": fruit.nutritional_info.vitamins
                    } if fruit.nutritional_info else None
                }
                for fruit in fruits
            ],
            "total_fruits": len(fruits),
            "total_suppliers": len(suppliers),
            "total_nutritional_records": len(nutritional_info)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 