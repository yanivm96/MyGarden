from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.db.database import get_db
from app.services.user_service import get_user_by_name, create_user, verify_password
from app.dependencies.auth import create_access_token
from app.schemas.user import UserCreate, UserResponse
from app.core.config import settings
from jose import jwt, JWTError

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/user/", response_model=UserResponse)
async def get_user_by_username(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = get_user_by_name(db, username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user  # Pydantic ימיר את האובייקט ל-JSON
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/token_login/", response_model=UserResponse)
async def login_with_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = get_user_by_name(db, username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login/", response_model=dict)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = get_user_by_name(db, user.username)
        if existing_user and verify_password(user.password, existing_user.password):
            access_token = create_access_token(data={"sub": user.username})
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {"username": existing_user.username, "id": existing_user.id}
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register/", response_model=dict)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user.username, user.password)
        if not new_user:
            raise HTTPException(status_code=400, detail="Error occurred during user creation")
        return {"success": "User has been created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
