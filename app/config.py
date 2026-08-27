from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FHIR Mock API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/fhir"
    HOST: str = "0.0.0.0"
    PORT: int = 9123


    CORS_ORIGINS: List[str]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings=Settings()
