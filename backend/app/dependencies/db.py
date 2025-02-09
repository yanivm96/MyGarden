from sqlalchemy.orm import Session
from app.db.database import get_db

def get_database() -> Session:
    return get_db()
