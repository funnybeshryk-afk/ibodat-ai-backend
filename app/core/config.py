from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "IBODAT AI Backend"
    DEBUG: bool = True

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"] # Adjust for production

    # Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
