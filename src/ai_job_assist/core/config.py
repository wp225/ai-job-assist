from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict()
    ANTHROPIC_KEY: str = Field()
    DEBUG: bool = False
    
settings = Settings()