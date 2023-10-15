import logging
from pydantic import SecretStr
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application settings read from environment variables.

    Attributes:
        db_url: Database connection URL.
        secret_key: Secret key used for token generation and verification.
        hashing_algorithm: Algorithm used for hashing (default: "HS256").
        access_token_expire_days: Duration of token validity in days (default: 7).
        google_oauth_client_id: Google OAuth2 client ID.
        google_oauth_client_secret: Google OAuth2 client secret.
    """
    environment: str
    db_url: str
    secret_key: SecretStr
    hashing_algorithm: str = "HS256"
    access_token_expire_days: int = 7

    secure_cookies: bool = True
    google_oauth_client_id: str
    google_oauth_client_secret: str

    frontend_base_url: str = 'http://localhost:3000'
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

# Ensuring essential settings are not empty/None.
assert settings.db_url and settings.secret_key and settings.google_oauth_client_id and settings.google_oauth_client_secret, "Essential settings can't be None or empty."

# Uncomment the following line to debug settings; ensure secrets are not logged.
# logger.debug(f"Settings: {settings.json()}")
