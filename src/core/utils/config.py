import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic.v1 import BaseSettings

load_dotenv()


class DBSettings(BaseModel):
    DB_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DB_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DB_NAME: str = os.getenv("DATABASE_NAME", "postgres")
    DB_USER: str = os.getenv("DATABASE_USER", "postgres")
    DB_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class TokenSettings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY")


class RunSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8002


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    token: TokenSettings = TokenSettings()
    run: RunSettings = RunSettings()


settings = Settings()
