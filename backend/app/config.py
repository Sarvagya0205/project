from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Full URL takes priority (Render/Railway inject this automatically)
    DATABASE_URL: Optional[str] = None

    # Individual fields used when DATABASE_URL is not set (local MySQL)
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "trello_clone"

    class Config:
        env_file = ".env"


settings = Settings()
