from sqlalchemy.orm import Session
from .database import engine, SessionLocal, Base
from .models import Fruit, NutritionalInfo, Supplier, FruitSupplier

# Create all tables
Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    try:
        # Add suppliers
        suppliers = [
            Supplier(name="Fresh Fruits Co", country="Spain", contact_email="contact@freshfruits.co", rating=4.8),
            Supplier(name="Tropical Harvest", country="Brazil", contact_email="sales@tropicalharvest.com", rating=4.5),
            Supplier(name="Global Fruits Ltd", country="New Zealand", contact_email="info@globalfruits.com", rating=4.7)
        ]
        for supplier in suppliers:
            db.add(supplier)
        db.commit()

        # Add fruits with nutritional info
        fruits_data = [
            {
                "fruit": Fruit(
                    name="Apple",
                    color="Red",
                    taste="Sweet",
                    origin_country="USA",
                    price_per_kg=2.5
                ),
                "nutrition": {
                    "calories": 52,
                    "carbohydrates": 14,
                    "protein": 0.3,
                    "fat": 0.2,
                    "fiber": 2.4,
                    "vitamins": "A, C, K"
                },
                "supplier_ids": [1, 3]
            },
            {
                "fruit": Fruit(
                    name="Banana",
                    color="Yellow",
                    taste="Sweet",
                    origin_country="Ecuador",
                    price_per_kg=1.8
                ),
                "nutrition": {
                    "calories": 89,
                    "carbohydrates": 23,
                    "protein": 1.1,
                    "fat": 0.3,
                    "fiber": 2.6,
                    "vitamins": "B6, C"
                },
                "supplier_ids": [2]
            },
            {
                "fruit": Fruit(
                    name="Orange",
                    color="Orange",
                    taste="Sweet-Citrus",
                    origin_country="Spain",
                    price_per_kg=2.0
                ),
                "nutrition": {
                    "calories": 47,
                    "carbohydrates": 12,
                    "protein": 0.9,
                    "fat": 0.1,
                    "fiber": 2.4,
                    "vitamins": "C, B1, Folate"
                },
                "supplier_ids": [1, 2]
            }
        ]

        for fruit_data in fruits_data:
            # Add fruit
            db.add(fruit_data["fruit"])
            db.flush()  # This will assign an ID to the fruit

            # Add nutritional info
            nutrition = NutritionalInfo(
                fruit_id=fruit_data["fruit"].id,
                **fruit_data["nutrition"]
            )
            db.add(nutrition)

            # Add supplier relationships
            for supplier_id in fruit_data["supplier_ids"]:
                fruit_supplier = FruitSupplier(
                    fruit_id=fruit_data["fruit"].id,
                    supplier_id=supplier_id
                )
                db.add(fruit_supplier)

        db.commit()

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 