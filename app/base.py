from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
Base.__name__ = 'Base'