from app.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://healthmate_qwqc_user:9n3GPfnf0J13AsHYbUYnydoUvjzoXVY2@dpg-ctgtokrtq21c73aba1f0-a.frankfurt-postgres.render.com/healthmate_qwqc",
)
#"postgresql://postgres:galena2612@localhost/healthmate",
# SQLAlchemy engine and session setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialize_database():
    """Initialize the database and create all tables."""
    Base.metadata.create_all(bind=engine)




def get_db():
    """Provide a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
