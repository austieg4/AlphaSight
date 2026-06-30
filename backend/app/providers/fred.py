import httpx

from app.config import settings


class FREDProvider:
    BASE_URL = "https://api.stlouisfed.org/fred"

    async def get_latest_observation(self, series_id: str):
        async with httpx.AsyncClient() as client:
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

        return {
            "series_id": series_id,
            "date": latest.get("date"),
            "value": latest.get("value"),
            "source": "fred",
        }

    async def get_macro_snapshot(self):
        return {
            "federal_funds_rate": await self.get_latest_observation("FEDFUNDS"),
            "ten_year_treasury": await self.get_latest_observation("DGS10"),
            "inflation_cpi": await self.get_latest_observation("CPIAUCSL"),
            "unemployment_rate": await self.get_latest_observation("UNRATE"),
        }