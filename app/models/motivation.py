from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import declarative_base
from app.database import Base

class Motivation(Base):
    __tablename__ = 'motivation'

    message_id = Column(Integer, primary_key=True)
    message = Column(Text)
    message_date = Column(Date)