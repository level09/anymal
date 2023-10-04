import logging
from pydantic_settings import BaseSettings  # Adjusted import
from pydantic import SecretStr

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Application settings read from environment variables.
    """
    db_url: str  # Using a URL to allow flexibility in DB choice
    secret_key: SecretStr
    hashing_algorithm: str = "HS256"
    access_token_expire_days: int = 7

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()

# Logging the settings for debugging purposes
#logger.debug(f"Settings: {settings.model_dump_json()}")
