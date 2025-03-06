from pydantic_settings import BaseSettings, SettingsConfigDict

class GlobalConfig(BaseSettings):
    """Configuration class"""
    llm_provider: str = "ollama"
    llm_model_name: str
    log_level: str = "INFO"

global_config = GlobalConfig()

