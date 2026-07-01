import httpx

from app.cache.memory_cache import memory_cache
from app.config import settings


class FMPProvider:
    BASE_URL = "https://financialmodelingprep.com/stable"

    async def get_company_profile(self, ticker: str):
        return await self._get_cached_endpoint(
            cache_key=f"fmp:profile:{ticker}",
            endpoint="profile",
            ticker=ticker,
        )

    async def get_key_metrics_ttm(self, ticker: str):
        return await self._get_cached_endpoint(
            cache_key=f"fmp:key-metrics-ttm:{ticker}",
            endpoint="key-metrics-ttm",
            ticker=ticker,
        )

    async def get_ratios_ttm(self, ticker: str):
        return await self._get_cached_endpoint(
            cache_key=f"fmp:ratios-ttm:{ticker}",
            endpoint="ratios-ttm",
            ticker=ticker,
        )

    async def get_financial_growth(self, ticker: str):
        return await self._get_cached_endpoint(
            cache_key=f"fmp:financial-growth:{ticker}",
            endpoint="financial-growth",
            ticker=ticker,
        )

    async def _get_cached_endpoint(
        self,
        cache_key: str,
        endpoint: str,
        ticker: str,
    ):
        cached_data = memory_cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        ) as client:
            response = await client.get(
                f"{self.BASE_URL}/{endpoint}",
                params={
                    "symbol": ticker,
                    "apikey": settings.FMP_API_KEY,
                },
            )

        response.raise_for_status()

        data = response.json()
        result = data[0] if data else None

        memory_cache.set(
            cache_key,
            result,
            settings.FMP_CACHE_TTL_SECONDS,
        )

        return result