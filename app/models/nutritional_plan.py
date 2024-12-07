from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database import Base
from sqlalchemy.orm import relationship


class NutritionalPlan(Base):
    __tablename__ = 'nutritional_plan'

    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    nutritionist = Column(Integer, ForeignKey('users.user_id'))
    calories = Column(Integer)
    protein = Column(Float)
    carbohydrates = Column(Float)
    fats = Column(Float)

    user = relationship('User', foreign_keys=[user_id], back_populates='nutritional_plans')
    nutritionist_user = relationship('User', foreign_keys=[nutritionist], back_populates='nutritionist_plans')
    meal_plan = relationship('MealPlan', back_populates='nutritional_plan', uselist=False)