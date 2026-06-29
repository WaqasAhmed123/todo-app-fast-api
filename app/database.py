from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# Use the configured DATABASE_URL from settings.
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Import models to register them with Base
from app.models.user import User  # noqa
from app.models.todo import Todo  # noqa

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()