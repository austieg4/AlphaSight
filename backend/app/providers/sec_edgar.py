import httpx

from app.config import settings


class SECEdgarProvider:
    TICKER_CIK_URL = "https://www.sec.gov/files/company_tickers.json"

    async def get_company(self, ticker: str):
        headers = {
            "User-Agent": settings.SEC_USER_AGENT or "AlphaSight/0.1 contact@example.com"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.TICKER_CIK_URL, headers=headers)

        response.raise_for_status()

        companies = response.json()
        clean_ticker = ticker.upper()

        for company in companies.values():
            if company.get("ticker", "").upper() == clean_ticker:
                cik_number = str(company.get("cik_str")).zfill(10)

                return {
                    "ticker": clean_ticker,
                    "company": company.get("title"),
                    "cik": cik_number,
                    "source": "sec_edgar",
                }

        return None