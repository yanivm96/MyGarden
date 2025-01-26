from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from ..database import get_db
from ..models import Plant
from ..crud import get_plant, get_all_user_plants, create_new_plant, get_user_by_name, delete_plant
import httpx
import os
import openai
import json
import re


openai.api_key = os.getenv("OPENAI_API_KEY")
PLANTID_API_KEY = os.getenv("PLANTID_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter()
db = next(get_db())


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
            headers={"Api-Key": PLANTID_API_KEY},
            json=request_body
        )

    if response.status_code == 201:
        data = response.json()
        if data.get("result", {}).get("classification", {}).get("suggestions"):
            name = data["result"]["classification"]["suggestions"][0]["name"]
            return name
        else:
            raise HTTPException(status_code=404, detail="No plant identified")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to identify plant")
    

async def get_chatgpt_response(plant_name : str) -> str:
    prompt = f"""
    You are a gardening expert assistant.
    Please provide the following structured information about the plant '{plant_name}':
    
    - **Description**: A short description (1-2 lines) summarizing the plant.
    - **Watering Instructions**: Short and clear (maximum one line).
    - **Sunny Hours**: Provide an **exact integer** indicating how many hours of sunlight this plant needs (only a single integer number).
    
    Return the information as a **pure JSON object** without any text or Markdown formatting. Only return the JSON object in this format:
    ```
    {{ "description": "<short description>",
      "watering": "<watering instructions>",
        "sunny_hours": <integer> }}

    - Make sure "sunny_hours" is a single **integer** value, not a string or a range.
    ```
    """

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    plant_info = response.choices[0].message["content"]
    try:
        plant_data = json.loads(plant_info)
        return plant_data
    except json.JSONDecodeError:
        raise ValueError("Response format from gpt is incorrect")


def get_user_from_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_by_name(db, username)
    
    return user

@router.post("/add_new_plant") 
async def add_new_plant(request: Request, token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    try:
        data = await get_and_validate_data_from_json_obj(request)
        image_base64 = check_base64(data)
        user = get_user_from_token(token)
        plant_name = await identify_plant(image_base64, data.get('latitude'), data.get('longitude'))
        plant_data = await get_chatgpt_response(plant_name)
        sunny_hours = 0
        if type(plant_data.get("sunny_hours")) is not int:
            sunny_hours = extract_integer_from_text(plant_data.get("sunny_hours"))
        else:
            sunny_hours = plant_data.get("sunny_hours")

        if plant_data:
            plant = create_new_plant(
                db, plant_name, user.id, plant_data.get("description"), data.get('image_base64'),
                plant_data.get('watering'), sunny_hours
            )

            if plant:
                return {"success": "Plant has been added"}, 200
            else:
                raise HTTPException(status_code=400, detail="Error occurred while creating plant")

    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(e)}
        )


def check_base64(data: dict):
    base64 = data.get('image_base64')
    if data.get('image_base64') is None:
        raise HTTPException(status_code=400, detail="image_base64 must not be empty")
    elif not data.get('image_base64').startswith("data:image"):
        base64 = f"data:image/jpeg;base64,{base64}"
    
    return base64

@router.get("/plant")
async def get_plant_by_id(request: Request):
    try:
        data = await get_and_validate_data_from_json_obj(request)
        plant = get_plant(db, data.get("plant_id"))
        if plant is not None:
            return plant_to_json(plant)
        
    except Exception as e:
        return {"error" : str(e)}  
    

@router.delete("/plant")
async def delete_plant_by_id(request: Request, token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    try:
        data = await get_and_validate_data_from_json_obj(request)
        user = get_user_from_token(token)
        if user is not None:
            plant = delete_plant(db, data.get("plant_id"))
            if plant is not None:
                return {"success": "Plant has been deleted"}, 200
            
            else:
                raise HTTPException(status_code=400, detail="Plant not found")

        else:
            raise HTTPException(status_code=400, detail="User not found")
    
    except Exception as e:
        return {"error" : str(e)}  
    

@router.get("/user_plants")
async def get_plant_by_id(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    try:
        user = get_user_from_token(token)
        if user is not None:
            plants = get_all_user_plants(db, user.id)
            return [plant_to_json(plant) for plant in plants]
        else:
            raise HTTPException(status_code=400, detail = "user not found")

    except Exception as e:
        return {"error" : str(e)}  


async def get_and_validate_data_from_json_obj(request: json) -> dict:
    data = await request.json()
    is_valid , key = validate_json_fields(data)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} must not be empty.")
    
    return data

def validate_json_fields(data: dict) -> bool:
    for key, value in data.items():
        if value in [None, "", [], {}]:  
            return False, key
    return True, None

def plant_to_json(plant: Plant) -> dict:
    if plant is None:
        return None
    
    return {key: value for key, value in plant.__dict__.items() if not key.startswith("_")}


def extract_integer_from_text(text):
    numbers = [int(num) for num in re.findall(r'\d+', text)]
    if len(numbers) == 1:
        return numbers[0]  
    elif len(numbers) > 1:
        return sum(numbers) // len(numbers)  
    else:
        raise ValueError("No valid sunny hours found")