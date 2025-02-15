from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app.core.config import settings
import os


engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

try:
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database '{engine.url.database}' created successfully!")
    else:
        print(f"Database '{engine.url.database}' already exists.")
except Exception as e:
    print(f"Error checking database existence: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    from app.models import Base
    Base.metadata.create_all(bind=engine)

init_db() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
