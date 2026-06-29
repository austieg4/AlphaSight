import httpx

from app.config import settings


class FinnhubProvider:
    BASE_URL = "https://finnhub.io/api/v1"

    async def get_company_profile(self, ticker: str):
        url = f"{self.BASE_URL}/stock/profile2"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={
                    "symbol": ticker,
                    "token": settings.FINNHUB_API_KEY,
                },
            )

        response.raise_for_status()

        data = response.json()

        if not data:
            return None

        return data