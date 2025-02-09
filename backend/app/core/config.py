from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str
    OPENAI_API_KEY: str
    PLANTID_API_KEY: str
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[str] = ["*"]  

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
