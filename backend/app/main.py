from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import user_router, plant_router
from app.core.config import settings
from app.db.database import init_db

app = FastAPI(debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(user_router, tags=["User"])
app.include_router(plant_router, tags=["Plant"])
