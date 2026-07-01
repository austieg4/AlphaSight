import httpx

from app.cache.memory_cache import memory_cache
from app.config import settings


class FinnhubProvider:
    BASE_URL = "https://finnhub.io/api/v1"

    async def get_company_profile(self, ticker: str):
        cache_key = f"finnhub:profile:{ticker}"

        cached_data = memory_cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        ) as client:
            response = await client.get(
                f"{self.BASE_URL}/stock/profile2",
                params={
                    "symbol": ticker,
                    "token": settings.FINNHUB_API_KEY,
                },
            )

        response.raise_for_status()

        data = response.json()

        result = data if data else None

        memory_cache.set(
            cache_key,
            result,
            settings.FINNHUB_CACHE_TTL_SECONDS,
        )

        return result