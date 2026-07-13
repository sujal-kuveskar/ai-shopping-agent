import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized Configuration Settings Engine.
    Automatically parses environment variables from the system environment or a .env file.
    """

    ENV: str = "development"
    PORT: int = 8000

    OPENAI_API_KEY: str
    BROWSERBASE_API_KEY: str
    BROWSERBASE_PROJECT_ID: str

    # Supabase Database Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            ".env"
        ),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()