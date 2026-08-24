from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "IBODAT AI Backend"
    DEBUG: bool = True

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"] # Adjust for production

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
