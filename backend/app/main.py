from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .crud import create_user, get_user_by_id
from .routes.plant import router as plant_router 
from .routes.user import router as user_router 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(debug= True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # מאפשר לכל המקורות (או רשום דומיינים ספציפיים)
    allow_credentials=True,
    allow_methods=["*"],  # מאפשר את כל סוגי הבקשות (GET, POST, PUT, DELETE וכו')
    allow_headers=["*"],  # מאפשר את כל סוגי הכותרות
)
app.include_router(user_router)
app.include_router(plant_router)


Base.metadata.create_all(bind=engine)


