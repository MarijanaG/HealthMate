from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import declarative_base, relationship
from app.database import Base

class Recipe(Base):
    __tablename__ = 'recipes'

    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    meal_plan_id = Column(Integer, ForeignKey('meal_plan.meal_plan_id'))
    name_receipe = Column(String)
    description = Column(Text)
    portion = Column(Float)
    calories = Column(Integer)
    carbohydrates = Column(Float)
    fats = Column(Float)
    type = Column(
        Enum('vegan', 'vegetarian', 'omnivorous', name='dietary_preference'),
        nullable=False)

    # Establish relationships
    meal_plan = relationship('MealPlan', back_populates='recipes')
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('User', back_populates='recipes')
