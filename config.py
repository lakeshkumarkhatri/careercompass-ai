from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings configuration."""
    app_name: str = "CareerCompass AI"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
