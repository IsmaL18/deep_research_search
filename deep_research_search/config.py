from pydantic import SecretStr
from pydantic_settings import BaseSettings

class GlobalConfig(BaseSettings):
    """Configuration class"""
    llm_provider: str = "ollama"
    llm_model_name: str
    log_level: str = "INFO"
    web_search_engine: str = "ddg"
    exa_search_api_key: SecretStr

global_config = GlobalConfig()

