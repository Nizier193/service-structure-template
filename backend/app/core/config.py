from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    HOST: str
    PORT: int

    DATABASE_URI: str

    class Config:
        env_file = ".env"

config = Config()