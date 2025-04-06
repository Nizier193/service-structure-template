from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    BACKEND_BASEURL: str
    TELEGRAM_TOKEN: str

    class Config:
        env_file = ".env"

config = Config()