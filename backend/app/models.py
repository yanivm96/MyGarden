# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from backend.app.db.database import Base
# from datetime import datetime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# import os 

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mydatabase")
# Base = declarative_base()
# engine = create_engine(DATABASE_URL)


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     username = Column(String(50), unique=True, index=True, nullable=False)
#     password = Column(String(255), nullable=False)
    
#     plants = relationship("Plant", back_populates="user", cascade="all, delete-orphan")


# class Plant(Base):
#     __tablename__ = "plants"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     name = Column(String, index=True)
#     description = Column(String)
#     image_base64 = Column(String)
#     watering = Column(String)
#     sunny_hours = Column(Integer)

#     user = relationship("User", back_populates="plants")

# Base.metadata.create_all(engine)