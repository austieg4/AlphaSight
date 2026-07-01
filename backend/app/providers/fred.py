import asyncio

import httpx

from app.cache.memory_cache import memory_cache
from app.config import settings


class FREDProvider:
    BASE_URL = "https://api.stlouisfed.org/fred"

    async def get_latest_observation(self, series_id: str):
        cache_key = f"fred:{series_id}"

        cached_data = memory_cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        ) as client:
            response = await client.get(
                f"{self.BASE_URL}/series/observations",
                params={
                    "series_id": series_id,
                    "api_key": settings.FRED_API_KEY,
                    "file_type": "json",
                    "sort_order": "desc",
                    "limit": 1,
                },
            )

        response.raise_for_status()

        data = response.json()
        observations = data.get("observations", [])

        if not observations:
            return None

        latest = observations[0]

        result = {
            "series_id": series_id,
            "date": latest.get("date"),
            "value": latest.get("value"),
            "source": "fred",
        }

        memory_cache.set(
            cache_key,
            result,
            settings.FRED_CACHE_TTL_SECONDS,
        )

        return result

    async def get_macro_snapshot(self):
        (
            federal_funds_rate,
            ten_year_treasury,
            inflation_cpi,
            unemployment_rate,
        ) = await asyncio.gather(
            self.get_latest_observation("FEDFUNDS"),
            self.get_latest_observation("DGS10"),
            self.get_latest_observation("CPIAUCSL"),
            self.get_latest_observation("UNRATE"),
        )

        return {
            "federal_funds_rate": federal_funds_rate,
            "ten_year_treasury": ten_year_treasury,
            "inflation_cpi": inflation_cpi,
            "unemployment_rate": unemployment_rate,
        }