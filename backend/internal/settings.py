from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/
BASE_DIR = Path(__file__).resolve().parent.parent


# .env file
class Settings(BaseSettings):
    debug: bool
    local: bool
    images_limit: int

    database_url: str

    exactly_api: str

    gcs_service_account_key_base64: str
    gs_bucket_name: str

    test_mode: bool = False

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")


settings = Settings()
