from app.providers.fmp import FMPProvider
from app.providers.finnhub import FinnhubProvider


class MarketDataService:
    def __init__(self):
        self.fmp_provider = FMPProvider()
        self.finnhub_provider = FinnhubProvider()

    async def get_company_overview(self, ticker: str):
        clean_ticker = ticker.upper()

        fmp_profile = await self.fmp_provider.get_company_profile(clean_ticker)
        finnhub_profile = await self.finnhub_provider.get_company_profile(clean_ticker)

        if fmp_profile is None and finnhub_profile is None:
            return None

        return {
            "ticker": clean_ticker,
            "company": (
                (fmp_profile or {}).get("companyName")
                or (finnhub_profile or {}).get("name")
            ),
            "price": (fmp_profile or {}).get("price"),
            "market_cap": (
                (fmp_profile or {}).get("marketCap")
                or (fmp_profile or {}).get("mktCap")
                or (finnhub_profile or {}).get("marketCapitalization")
            ),
            "sector": (fmp_profile or {}).get("sector"),
            "industry": (
                (fmp_profile or {}).get("industry")
                or (finnhub_profile or {}).get("finnhubIndustry")
            ),
            "website": (
                (fmp_profile or {}).get("website")
                or (finnhub_profile or {}).get("weburl")
            ),
            "summary": (fmp_profile or {}).get("description"),
            "sources": {
                "fmp_profile": fmp_profile is not None,
                "finnhub_profile": finnhub_profile is not None,
            },
            "confidence": {
                "company_profile": 0.9 if fmp_profile and finnhub_profile else 0.75
            },
            "status": "multi_source_market_data_service",
        }