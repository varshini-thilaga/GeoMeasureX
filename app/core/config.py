from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAX_UPLOAD_BYTES: int = 50 * 1024 * 1024
    MAX_ZIP_FILES: int = 50
    MAX_UNCOMPRESSED_BYTES: int = 500 * 1024 * 1024
    MAX_COMPRESSION_RATIO: int = 100
    MAX_PAGE_SIZE: int = 500
    DEFAULT_PAGE_SIZE: int = 50
    DATABASE_URL: str = "sqlite:///./geomeasurex.db"
    LOG_LEVEL: str = "INFO"
    TEMP_DIR: str = "./temp_uploads"

    class Config:
        env_prefix = "GEOMEASUREX_"

settings = Settings()
