from sqlalchemy.orm import Session
from models import User, Plant
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, username: str, password: str) -> User:
    validate_input_fields([username,password])
    user = User(username=username, password=hash_password(password))
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Username '{username}' already exists.")
    return user

def get_user_by_id(db: Session, id: int) -> User:
    return db.query(User).filter(User.id == id).first()

def get_user_by_name(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def create_new_plant(db: Session, plant_name: str, user_id: int ,plant_description: str, image_base64: str, watering: str, sunny_hours: int) -> Plant:
    validate_input_fields([plant_name, user_id, plant_description, image_base64, watering, sunny_hours])
    plant = Plant(name= plant_name, user_id=user_id, description=plant_description, image_base64=image_base64, watering=watering, sunny_hours=sunny_hours)
    try:
        db.add(plant)
        db.commit()
        db.refresh(plant)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Plant '{plant_name}' already exists.")
    return plant


def get_plant(db:Session, id: int) -> Plant:
    return db.query(Plant).filter(id==id).first()


def get_all_user_plants(db:Session, user_id) -> list:
    return db.query(Plant).filter(Plant.user_id == user_id).all()

def delete_plant(db:Session, id: int) -> Plant:
    plant = db.query(Plant).filter(Plant.id == id).first()
    db.delete(plant)
    db.commit()
    return plant


def validate_input_fields(inputs: list):
    for input in inputs:
        if not input:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{input} must not be empty."
            )
        

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)