from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    app_env: str = "dev"
    rule_reload_seconds: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
