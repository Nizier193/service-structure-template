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
    
    # API Keys
    SERVICE_API_KEY: str = "service-key-change-me"
    ADMIN_API_KEY: str = "admin-key-change-me"

    class Config:
        env_file = ".env"

config = Config()