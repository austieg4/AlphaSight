import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


settings = Settings()