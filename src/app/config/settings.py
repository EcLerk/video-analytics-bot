from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE__", env_file=".env")

    user: str = None
    password: str = None
    name: str = None

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@db:5432/{self.name}"


class TGBotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TG__", env_file=".env")

    api_key: str = None


class OpenAISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OPENAI__", env_file=".env")

    api_key: str = None


class Settings(BaseSettings):
    database_settings: DBSettings = DBSettings()
    tg_bot_settings: TGBotSettings = TGBotSettings()
    openai_settings: OpenAISettings = OpenAISettings()


settings = Settings()
