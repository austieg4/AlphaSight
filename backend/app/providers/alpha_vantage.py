import httpx

from app.config import settings


class AlphaVantageProvider:
    BASE_URL = "https://www.alphavantage.co/query"

    async def get_global_quote(self, ticker: str):
        async with httpx.AsyncClient() as client:
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

        return {
            "symbol": quote.get("01. symbol"),
            "price": quote.get("05. price"),
            "change_percent": quote.get("10. change percent"),
            "source": "alpha_vantage",
        }