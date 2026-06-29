import httpx

from app.config import settings


class FMPProvider:
    BASE_URL = "https://financialmodelingprep.com/stable"

    async def get_company_profile(self, ticker: str):
        url = f"{self.BASE_URL}/profile"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={
                    "symbol": ticker,
                    "apikey": settings.FMP_API_KEY,
                },
            )

        response.raise_for_status()

        data = response.json()

        if not data:
            return None

        return data[0]