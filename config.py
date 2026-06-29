from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "CareerCompass AI"
    google_api_key: str
    model_name: str = "gemini-1.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",   # Ignore unrelated environment variables
    )

settings = Settings()