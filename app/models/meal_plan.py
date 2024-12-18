from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from app.database import Base

class MealPlan(Base):
    __tablename__ = 'meal_plan'

    meal_plan_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey('nutritional_plan.plan_id', ondelete='CASCADE'))
    description = Column(String, nullable=True)
    start_date = Column(Date)
    end_date = Column(Date)

    nutritional_plan = relationship('NutritionalPlan', back_populates='meal_plan')
