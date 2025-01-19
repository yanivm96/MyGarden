from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from ..database import get_db
from ..models import Plant
from ..crud import get_plant, get_all_user_plants, create_new_plant
import httpx
import os
import openai
import json
import re


openai.api_key = os.getenv("OPENAI_API_KEY")
PLANTID_API_KEY = os.getenv("PLANTID_API_KEY")

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
    

# async def identify_plant(plant_name):
#     try:
#         if plant_name is not None:
#             return {"plant_name": plant_name, 
#                     "info": get_chatgpt_response(plant_name)}, 200
#         else:
#             return {"error": "invalid plant name"}, 400

#     except HTTPException as e:
#         raise e  

#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": "Internal server error", "detail": str(e)}
#         )
    

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




@router.post("/add_new_plant")
async def add_new_plant(request: Request):
    try:
        data = await get_and_validate_data_from_json_obj(request)
        plant_name = await identify_plant(data.get('image_base64'), data.get('latitude'), data.get('longitude'))
        plant_data = await get_chatgpt_response(plant_name)
        sunny_hours = 0
        if type(plant_data.get("sunny_hours")) is not int:
            sunny_hours = extract_integer_from_text(plant_data.get("sunny_hours"))
        else:
            sunny_hours = plant_data.get("sunny_hours")

        if plant_data:
            plant = create_new_plant(
                db, plant_name, data.get('user_id'), plant_data.get("description"), data.get('image_base64'),
                plant_data.get('watering'), sunny_hours
            )

            if plant:
                return {"success": "Plant has been added"}
            else:
                raise HTTPException(status_code=400, detail="Error occurred while creating plant")

    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(e)}
        )


@router.get("/plant")
async def get_plant_by_id(request: Request):
    try:
        data = await get_and_validate_data_from_json_obj(request)
        plant = get_plant(db, data.get("plant_id"))
        if plant is not None:
            return plant_to_json(plant)
        
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