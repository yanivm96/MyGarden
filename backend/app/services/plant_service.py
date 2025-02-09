from sqlalchemy.orm import Session
from app.models.plant import Plant
from app.schemas.plant import PlantCreate
from app.core.config import settings
import httpx
import openai
import json

openai.api_key = settings.OPENAI_API_KEY

async def identify_plant(image_base64: str, latitude: float = None, longitude: float = None, similar_images: bool = True):
    request_body = {
        "images": [image_base64],
        "similar_images": similar_images
    }

    if latitude and longitude:
        request_body["latitude"] = latitude
        request_body["longitude"] = longitude

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.plant.id/v3/identification",
            headers={"Api-Key": settings.PLANTID_API_KEY},
            json=request_body
        )

    if response.status_code == 201:
        data = response.json()
        if data.get("result", {}).get("classification", {}).get("suggestions"):
            name = data["result"]["classification"]["suggestions"][0]["name"]
            return name
        else:
            raise ValueError("No plant identified")
    else:
        raise ValueError("Failed to identify plant")

async def get_chatgpt_response(plant_name: str) -> dict:
    prompt = f"""
    You are a gardening expert assistant.
    Please provide the following structured information about the plant '{plant_name}':
    
    - **Description**: A short description (1-2 lines).
    - **Watering Instructions**: Maximum one line.
    - **Sunny Hours**: An exact integer value of sunlight hours required.

    Return a pure JSON object:
    {{
        "description": "<short description>",
        "watering": "<watering instructions>",
        "sunny_hours": <integer>
    }}
    """

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response.choices[0].message["content"])
    except json.JSONDecodeError:
        raise ValueError("Invalid response from ChatGPT")

def create_new_plant(db: Session, name: str, user_id: int, description: str, image_base64: str, watering: str, sunny_hours: int):
    plant = Plant(
        name=name,
        user_id=user_id,
        description=description,
        image_base64=image_base64,
        watering=watering,
        sunny_hours=sunny_hours
    )
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant

def get_plant(db: Session, plant_id: int):
    return db.query(Plant).filter(Plant.id == plant_id).first()

def delete_plant(db: Session, plant_id: int):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant:
        db.delete(plant)
        db.commit()
        return True
    return False

def get_all_user_plants(db: Session, user_id: int):
    return db.query(Plant).filter(Plant.user_id == user_id).all()
