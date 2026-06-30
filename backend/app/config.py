import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    SEC_USER_AGENT = os.getenv("SEC_USER_AGENT")
    FRED_API_KEY = os.getenv("FRED_API_KEY")


settings = Settings()