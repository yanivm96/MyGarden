from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.db.database import get_db
from app.schemas.plant import PlantCreate, PlantResponse
from app.services.plant_service import create_new_plant, get_plant, delete_plant, get_all_user_plants, identify_plant, get_chatgpt_response
from app.dependencies.auth import get_user_from_token
from app.utils.helpers import extract_integer_from_text, check_base64

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/add_new_plant", response_model=PlantResponse)
async def add_new_plant(plant: PlantCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        image_base64 = check_base64({"image_base64": plant.image_base64})
        user = get_user_from_token(token, db)
        plant_name = await identify_plant(image_base64, plant.latitude, plant.longitude)
        plant_data = await get_chatgpt_response(plant_name)

        sunny_hours = plant_data.get("sunny_hours", 0)
        if not isinstance(sunny_hours, int):
            sunny_hours = extract_integer_from_text(str(sunny_hours))

        new_plant = create_new_plant(
            db, plant_name, user.id, plant_data.get("description"), image_base64, plant_data.get("watering"), sunny_hours
        )
        return new_plant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plant", response_model=PlantResponse)
async def get_plant_by_id(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        plant_id = data.get("plant_id")
        if not plant_id:
            raise HTTPException(status_code=400, detail="Plant ID is required")
        
        plant = get_plant(db, plant_id)
        if not plant:
            raise HTTPException(status_code=404, detail="Plant not found")
        return plant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/plant", status_code=204)
async def delete_plant_by_id(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        data = await request.json()
        plant_id = data.get("plant_id")
        if not plant_id:
            raise HTTPException(status_code=400, detail="Plant ID is required")

        user = get_user_from_token(token, db)
        if user:
            success = delete_plant(db, plant_id)
            if not success:
                raise HTTPException(status_code=404, detail="Plant not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user_plants", response_model=list[PlantResponse])
async def get_all_user_plants_by_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user = get_user_from_token(token, db)
        if user:
            plants = get_all_user_plants(db, user.id)
            return plants
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
