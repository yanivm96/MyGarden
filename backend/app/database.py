from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os

load_dotenv(dotenv_path="/home/ubuntu/MyGarden/MyGarden/backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)
    print(f"Database {engine.url.database} created successfully!")
else:
    print(f"Database {engine.url.database} already exists.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
