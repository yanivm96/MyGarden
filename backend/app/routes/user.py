from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from ..models import User
from ..crud import get_user_by_id, create_user, verify_password, get_user_by_name
from ..database import get_db
from ...utils import create_access_token
import json
import os

router = APIRouter()
db = next(get_db())
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@router.get("/user/")
async def get_user_by_username(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = get_user_by_name(db, username)
        if user is not None:
            return user_to_json(user), 200
        else:
            raise HTTPException(status_code=400, detail = "user not found")
    
    except HTTPException as e:
        raise e  
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(e)}
        )

@router.post("/token_login/")
async def login(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = get_user_by_name(db, username)
        if user is not None:
            return user_to_json(user), 200
        else:
            raise HTTPException(status_code=400, detail = "user not found")
    
    except HTTPException as e:
        raise e  
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(e)}
        )


@router.post("/login/")
async def login(request: Request):
    try:
        data = await get_and_validate_data_from_json_obj(request)
        user = get_user_by_name(db, data.get("username"))
        if user is not None and verify_password(data.get("password"), user.password):
            access_token = create_access_token(data={"sub": data.get("username")})

            return {"access_token": access_token,
                     "token_type": "bearer",
                     "user": user}, 200
        else:
            raise HTTPException(status_code=400, detail = "user not found")


    except HTTPException as e:
        raise e  

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(e)}
        )

@router.post("/register/")
async def create_new_user(request: Request):
    try:
        data = await get_and_validate_data_from_json_obj(request)
        user = create_user(db, data.get("username"), data.get("password"))
        if user is not None:
            return {"success": "user has been created"}, 200
        else:
            raise HTTPException(status_code=400, detail = "error occurred")
        
    except HTTPException as e:
        raise e  

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(e)}
        )



def validate_json_fields(data: dict) -> bool:
    for key, value in data.items():
        if value in [None, "", [], {}]:  
            return False, key
    return True, None

def user_to_json(user: User) -> dict:
    if user is None:
        return {}
    return {key: value for key, value in user.__dict__.items() if not key.startswith("_")}

async def get_and_validate_data_from_json_obj(request: json) -> dict:
    data = await request.json()
    is_valid , key = validate_json_fields(data)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} must not be empty.")
        
    return data
    