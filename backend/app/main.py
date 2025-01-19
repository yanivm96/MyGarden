from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .crud import create_user, get_user
from .routes.plant import router as plant_router 
from .routes.user import router as user_router 


app = FastAPI(debug= True)

app.include_router(user_router)
app.include_router(plant_router)


Base.metadata.create_all(bind=engine)


