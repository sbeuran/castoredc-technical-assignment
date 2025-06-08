from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Fruit(Base):
    __tablename__ = "fruits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    color = Column(String(50))
    taste = Column(String(50))
    origin_country = Column(String(100))
    price_per_kg = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    nutritional_info = relationship("NutritionalInfo", back_populates="fruit", uselist=False)
    suppliers = relationship("Supplier", secondary="fruit_suppliers", back_populates="fruits")

class NutritionalInfo(Base):
    __tablename__ = "nutritional_info"

    id = Column(Integer, primary_key=True, index=True)
    fruit_id = Column(Integer, ForeignKey("fruits.id"))
    calories = Column(Integer)
    carbohydrates = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    fiber = Column(Float)
    vitamins = Column(String(200))

    fruit = relationship("Fruit", back_populates="nutritional_info")

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    country = Column(String(100))
    contact_email = Column(String(100))
    rating = Column(Float)

    fruits = relationship("Fruit", secondary="fruit_suppliers", back_populates="suppliers")

class FruitSupplier(Base):
    __tablename__ = "fruit_suppliers"

    fruit_id = Column(Integer, ForeignKey("fruits.id"), primary_key=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), primary_key=True) 