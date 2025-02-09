# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status
# from passlib.context import CryptContext
# from app.models import User, Plant

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def create_user(db: Session, username: str, password: str) -> User:
#     validate_input_fields([username, password])
#     user = User(username=username, password=hash_password(password))
#     try:
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#         return user
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Username '{username}' already exists."
#         )

# def get_user_by_id(db: Session, id: int) -> User:
#     user = db.query(User).filter(User.id == id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with ID {id} not found."
#         )
#     return user

# def get_user_by_name(db: Session, username: str) -> User:
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with username '{username}' not found."
#         )
#     return user

# def create_new_plant(
#     db: Session, plant_name: str, user_id: int, plant_description: str,
#     image_base64: str, watering: str, sunny_hours: int
# ) -> Plant:
#     validate_input_fields([plant_name, user_id, plant_description, image_base64, watering, sunny_hours])
#     plant = Plant(
#         name=plant_name,
#         user_id=user_id,
#         description=plant_description,
#         image_base64=image_base64,
#         watering=watering,
#         sunny_hours=sunny_hours
#     )
#     try:
#         db.add(plant)
#         db.commit()
#         db.refresh(plant)
#         return plant
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Plant '{plant_name}' already exists."
#         )

# def get_plant(db: Session, id: int) -> Plant:
#     plant = db.query(Plant).filter(Plant.id == id).first()
#     if not plant:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Plant with ID {id} not found."
#         )
#     return plant

# def get_all_user_plants(db: Session, user_id: int) -> list:
#     plants = db.query(Plant).filter(Plant.user_id == user_id).all()
#     if not plants:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"No plants found for user with ID {user_id}."
#         )
#     return plants

# def delete_plant(db: Session, id: int) -> Plant:
#     plant = db.query(Plant).filter(Plant.id == id).first()
#     if not plant:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Plant with ID {id} not found."
#         )
#     db.delete(plant)
#     db.commit()
#     return plant

# def validate_input_fields(inputs: list):
#     for input in inputs:
#         if not input:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Input fields must not be empty."
#             )

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
