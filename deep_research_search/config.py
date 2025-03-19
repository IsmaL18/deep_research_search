from pydantic import SecretStr
from pydantic_settings import BaseSettings

class GlobalConfig(BaseSettings):
    """Configuration class"""
    llm_provider: str
    llm_model_name: str
    log_level: str 
    web_search_engine: str
    exa_search_api_key: SecretStr

global_config = GlobalConfig()

