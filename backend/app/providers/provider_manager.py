import asyncio

from app.providers.alpha_vantage import AlphaVantageProvider
from app.providers.finnhub import FinnhubProvider
from app.providers.fmp import FMPProvider
from app.providers.fred import FREDProvider
from app.providers.sec_edgar import SECEdgarProvider


class ProviderManager:
    """
    Coordinates external market data providers.
    """

    def __init__(self):
        self.fmp_provider = FMPProvider()
        self.finnhub_provider = FinnhubProvider()
        self.alpha_vantage_provider = AlphaVantageProvider()
        self.sec_provider = SECEdgarProvider()
        self.fred_provider = FREDProvider()

    async def fetch_company_data(self, ticker: str):
        results = await asyncio.gather(
            self.fmp_provider.get_company_profile(ticker),
            self.fmp_provider.get_key_metrics_ttm(ticker),
            self.fmp_provider.get_ratios_ttm(ticker),
            self.fmp_provider.get_financial_growth(ticker),
            self.finnhub_provider.get_company_profile(ticker),
            self.alpha_vantage_provider.get_global_quote(ticker),
            self.sec_provider.get_company(ticker),
            self.fred_provider.get_macro_snapshot(),
            return_exceptions=True,
        )

        return {
            "fmp_profile": self._clean_result(results[0]),
            "fmp_key_metrics": self._clean_result(results[1]),
            "fmp_ratios": self._clean_result(results[2]),
            "fmp_growth": self._clean_result(results[3]),
            "finnhub_profile": self._clean_result(results[4]),
            "alpha_vantage_quote": self._clean_result(results[5]),
            "sec_company": self._clean_result(results[6]),
            "macro_snapshot": self._clean_result(results[7]),
        }

    def _clean_result(self, result):
        if isinstance(result, Exception):
            return None

        return result