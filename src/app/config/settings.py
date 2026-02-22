from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE__", env_file=".env")

    user: str = None
    password: str = None
    name: str = None

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@db:5432/{self.name}"


class Settings(BaseSettings):
    database_settings: DBSettings = DBSettings()


settings = Settings()
