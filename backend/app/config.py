from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FMP_API_KEY: str
    FINNHUB_API_KEY: str
    ALPHA_VANTAGE_API_KEY: str
    FRED_API_KEY: str
    SEC_USER_AGENT: str

    FRONTEND_ORIGIN: str = "http://localhost:3000"

    REQUEST_TIMEOUT_SECONDS: int = 20
    PROVIDER_RETRY_COUNT: int = 2

    FMP_CACHE_TTL_SECONDS: int = 60 * 60 * 6
    FINNHUB_CACHE_TTL_SECONDS: int = 60 * 60 * 6
    ALPHA_VANTAGE_CACHE_TTL_SECONDS: int = 60 * 60 * 6
    FRED_CACHE_TTL_SECONDS: int = 60 * 60 * 12
    SEC_CACHE_TTL_SECONDS: int = 60 * 60 * 24

    DEVELOPMENT_PEER_LIMIT: int = 2

    LOG_PROVIDER_ERRORS: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()