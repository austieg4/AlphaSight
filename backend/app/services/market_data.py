import asyncio

from app.models.company import CompanyOverview
from app.providers.alpha_vantage import AlphaVantageProvider
from app.providers.finnhub import FinnhubProvider
from app.providers.fmp import FMPProvider
from app.providers.fred import FREDProvider
from app.providers.sec_edgar import SECEdgarProvider


class MarketDataService:
    def __init__(self):
        self.fmp_provider = FMPProvider()
        self.finnhub_provider = FinnhubProvider()
        self.alpha_vantage_provider = AlphaVantageProvider()
        self.sec_provider = SECEdgarProvider()
        self.fred_provider = FREDProvider()

    async def get_company_overview(self, ticker: str):
        clean_ticker = ticker.upper()

        results = await asyncio.gather(
            self.fmp_provider.get_company_profile(clean_ticker),
            self.finnhub_provider.get_company_profile(clean_ticker),
            self.alpha_vantage_provider.get_global_quote(clean_ticker),
            self.sec_provider.get_company(clean_ticker),
            self.fred_provider.get_macro_snapshot(),
            return_exceptions=True,
        )

        fmp_profile, finnhub_profile, alpha_vantage_quote, sec_company, macro_snapshot = [
            None if isinstance(result, Exception) else result
            for result in results
        ]

        if (
            fmp_profile is None
            and finnhub_profile is None
            and alpha_vantage_quote is None
            and sec_company is None
        ):
            return None

        return CompanyOverview(
            ticker=clean_ticker,
            company=(
                (fmp_profile or {}).get("companyName")
                or (finnhub_profile or {}).get("name")
                or (sec_company or {}).get("company")
                or (alpha_vantage_quote or {}).get("symbol")
            ),
            price=(
                (fmp_profile or {}).get("price")
                or (alpha_vantage_quote or {}).get("price")
            ),
            market_cap=(
                (fmp_profile or {}).get("marketCap")
                or (fmp_profile or {}).get("mktCap")
                or (finnhub_profile or {}).get("marketCapitalization")
            ),
            sector=(fmp_profile or {}).get("sector"),
            industry=(
                (fmp_profile or {}).get("industry")
                or (finnhub_profile or {}).get("finnhubIndustry")
            ),
            website=(
                (fmp_profile or {}).get("website")
                or (finnhub_profile or {}).get("weburl")
            ),
            summary=(fmp_profile or {}).get("description"),
            sources={
                "fmp_profile": fmp_profile is not None,
                "finnhub_profile": finnhub_profile is not None,
                "alpha_vantage_quote": alpha_vantage_quote is not None,
                "sec_company": sec_company is not None,
                "fred_macro": macro_snapshot is not None,
            },
            confidence={
                "company_profile": 0.95 if fmp_profile and finnhub_profile and sec_company else 0.8,
                "price": 0.9 if fmp_profile and alpha_vantage_quote else 0.75,
                "macro_context": 0.9 if macro_snapshot else 0.0,
            },
            status="concurrent_five_source_market_data_service",
        )