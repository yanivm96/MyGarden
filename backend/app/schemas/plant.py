from pydantic import BaseModel
from typing import Optional

class PlantBase(BaseModel):
    pass

class PlantCreate(PlantBase):
    image_base64: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PlantResponse(PlantBase):
    id: int
    image_base64: str
    name: Optional[str] = None
    description: Optional[str] = None
    watering: Optional[str] = None
    sunny_hours: Optional[int] = None

    class Config:
        from_attributes = True
