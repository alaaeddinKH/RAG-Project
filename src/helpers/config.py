from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME : str 
    APP_VERSION : str

    FILE_ALLOWD_TYPES : list
    FILE_MAX_SIZE : int
    FILE_DEFULT_CHUNKS_SIZE : int

    MONGODB_URL : str
    MONGODB_DATABASE : str

    class Config:
        env_file = "src/.env"


def get_settings():
    return Settings()