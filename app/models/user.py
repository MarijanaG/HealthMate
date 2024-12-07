from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, declarative_base, relationship
from app.schemas import UserCreate
from app.database import get_db, Base
from sqlalchemy import Column, Integer, String, Float, Enum


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    e_mail = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    preference = Column(
        Enum('vegan', 'vegetarian', 'omnivorous', name='dietary_preference'),
        nullable=False
    )
    user_type = Column(
        Enum('Nutritionist', 'Client', name='user_roles'),
        nullable=False
    )

    # Relationships
    nutritional_plans = relationship(
        'NutritionalPlan',
        foreign_keys='NutritionalPlan.user_id',
        back_populates='user'
    )
    nutritionist_plans = relationship(
        'NutritionalPlan',
        foreign_keys='NutritionalPlan.nutritionist',
        back_populates='nutritionist_user'
    )




