import logging
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application settings read from environment variables.

    Attributes:
        domain: The domain where your application is hosted.
        db_url: Database connection URL.
        secret_key: Secret key used for token generation and verification.
        hashing_algorithm: Algorithm used for hashing (default: "HS256").
        access_token_expire_days: Duration of token validity in days (default: 7).
        google_oauth_client_id: Google OAuth2 client ID.
        google_oauth_client_secret: Google OAuth2 client secret.
        stripe_secret_key: Your Stripe secret API key.
        webhook_secret: Your Stripe webhook secret (used for verifying webhook signatures).

    """
    domain: str
    environment: str
    db_url: str
    secret_key: SecretStr
    hashing_algorithm: str = "HS256"
    access_token_expire_days: int = 7
    debug: bool = False

    secure_cookies: bool = True
    google_oauth_client_id: str
    google_oauth_client_secret: str

    frontend_base_url: str = 'http://localhost:3000'

    # Stripe Configuration
    stripe_publishable_key: SecretStr
    stripe_secret_key: SecretStr
    webhook_secret: str
    auth_cookie_name: str = 'anymal'
    docs_url: Optional[str] = '/docs' if not debug else None
    redoc_url: Optional[str] = '/redoc' if not debug else None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

# Ensuring essential settings are not empty/None.
essential_settings = [
    settings.db_url,
    settings.secret_key,
    settings.google_oauth_client_id,
    settings.google_oauth_client_secret,
    settings.stripe_secret_key,
    settings.webhook_secret
]
assert all(essential_settings), "Essential settings can't be None or empty."

# Uncomment the following line to debug settings; ensure secrets are not logged.
# logger.debug(f"Settings: {settings.json()}")
