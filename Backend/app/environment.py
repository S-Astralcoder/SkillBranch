from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    JWT_SECRET_KEY: str = ""
    EXPIRATION_MINUTE: int = 15
    EXPIRATION_HOUR: int = 0
    EXPIRATION_DAY: int = 0
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
