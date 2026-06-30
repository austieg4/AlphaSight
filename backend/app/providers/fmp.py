import httpx

from app.config import settings


class FMPProvider:
    BASE_URL = "https://financialmodelingprep.com/stable"

    async def get_company_profile(self, ticker: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/profile",
                params={
                    "symbol": ticker,
                    "apikey": settings.FMP_API_KEY,
                },
            )

        response.raise_for_status()

        data = response.json()
        return data[0] if data else None

    async def get_key_metrics_ttm(self, ticker: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/key-metrics-ttm",
                params={
                    "symbol": ticker,
                    "apikey": settings.FMP_API_KEY,
                },
            )

        response.raise_for_status()

        data = response.json()
        return data[0] if data else None

    async def get_ratios_ttm(self, ticker: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/ratios-ttm",
                params={
                    "symbol": ticker,
                    "apikey": settings.FMP_API_KEY,
                },
            )

        response.raise_for_status()

        data = response.json()
        
        return data[0] if data else None