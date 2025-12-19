from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    HOST: str
    PORT: int

    CACHE_HOST: str
    CACHE_PORT: int

    DATABASE_URI: str
    LOG_LEVEL: str
    
    # JWT настройки
    JWT_SECRET_KEY: str = "your-secret-key-change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

config = Config()