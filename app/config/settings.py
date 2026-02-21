from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE__", env_file=".env")

    url: str = None


class Settings(BaseSettings):
    database_settings: DBSettings = DBSettings()


settings = Settings()
