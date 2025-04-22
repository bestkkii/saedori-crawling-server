# 예시
from pydantic import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = True
    APP_NAME: str = "MyApp"

    class Config:
        env_file = ".env"

settings = Settings()