import httpx

from app.cache.memory_cache import memory_cache
from app.config import settings


class SECEdgarProvider:
    TICKER_CIK_URL = "https://www.sec.gov/files/company_tickers.json"

    async def get_company(self, ticker: str):
        clean_ticker = ticker.upper()
        cache_key = f"sec:company:{clean_ticker}"

        cached_data = memory_cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        headers = {
            "User-Agent": settings.SEC_USER_AGENT
        }

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        ) as client:
            response = await client.get(
                self.TICKER_CIK_URL,
                headers=headers,
            )

        response.raise_for_status()

        companies = response.json()

        for company in companies.values():
            if company.get("ticker", "").upper() == clean_ticker:
                cik_number = str(company.get("cik_str")).zfill(10)

                result = {
                    "ticker": clean_ticker,
                    "company": company.get("title"),
                    "cik": cik_number,
                    "source": "sec_edgar",
                }

                memory_cache.set(
                    cache_key,
                    result,
                    settings.SEC_CACHE_TTL_SECONDS,
                )

                return result

        memory_cache.set(
            cache_key,
            None,
            settings.SEC_CACHE_TTL_SECONDS,
        )

        return None