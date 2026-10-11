from pydantic_settings import BaseSettings,SettingsConfigDict 

class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file=".env")
    db_echo: bool = False
settings = Settings()