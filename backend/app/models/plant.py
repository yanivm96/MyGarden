from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True)
    description = Column(String)
    image_base64 = Column(String)
    watering = Column(String)
    sunny_hours = Column(Integer)

    user = relationship("User", back_populates="plants")
