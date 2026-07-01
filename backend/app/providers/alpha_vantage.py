import httpx

from app.cache.memory_cache import memory_cache
from app.config import settings


class AlphaVantageProvider:
    BASE_URL = "https://www.alphavantage.co/query"

    async def get_global_quote(self, ticker: str):
        cache_key = f"alpha_vantage:quote:{ticker}"

        cached_data = memory_cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        ) as client:
            response = await client.get(
                self.BASE_URL,
                params={
                    "function": "GLOBAL_QUOTE",
                    "symbol": ticker,
                    "apikey": settings.ALPHA_VANTAGE_API_KEY,
                },
            )

        response.raise_for_status()

        data = response.json()
        quote = data.get("Global Quote")

        if not quote:
            return None

        result = {
            "symbol": quote.get("01. symbol"),
            "price": quote.get("05. price"),
            "change_percent": quote.get("10. change percent"),
            "source": "alpha_vantage",
        }

        memory_cache.set(
            cache_key,
            result,
            settings.ALPHA_VANTAGE_CACHE_TTL_SECONDS,
        )

        return result