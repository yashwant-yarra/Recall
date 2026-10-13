from pydantic_settings import BaseSettings,SettingsConfigDict 

class Settings(BaseSettings):
    database_url: str
    gcs_bucket: str
    model_config = SettingsConfigDict(env_file=".env")
    db_echo: bool = False
    dev_user_id: str | None = None
    max_upload_size: int = 25 * 1024 * 1024  # 25 MB
    upload_url_ttl_seconds: int = 15 * 60  # 15 minutes


settings = Settings()