import asyncio

from app.providers.alpha_vantage import AlphaVantageProvider
from app.providers.finnhub import FinnhubProvider
from app.providers.fmp import FMPProvider
from app.providers.fred import FREDProvider
from app.providers.provider_registry import ProviderRegistry
from app.providers.sec_edgar import SECEdgarProvider


class ProviderManager:
    """
    Coordinates external market data providers.
    """

    def __init__(self):
        self.registry = ProviderRegistry()

        self.registry.register("fmp", FMPProvider())
        self.registry.register("finnhub", FinnhubProvider())
        self.registry.register("alpha_vantage", AlphaVantageProvider())
        self.registry.register("sec", SECEdgarProvider())
        self.registry.register("fred", FREDProvider())

    async def fetch_company_data(self, ticker: str):
        fmp = self.registry.get("fmp")
        finnhub = self.registry.get("finnhub")
        alpha_vantage = self.registry.get("alpha_vantage")
        sec = self.registry.get("sec")
        fred = self.registry.get("fred")

        results = await asyncio.gather(
            fmp.get_company_profile(ticker),
            fmp.get_key_metrics_ttm(ticker),
            fmp.get_ratios_ttm(ticker),
            fmp.get_financial_growth(ticker),
            finnhub.get_company_profile(ticker),
            alpha_vantage.get_global_quote(ticker),
            sec.get_company(ticker),
            fred.get_macro_snapshot(),
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

    def provider_names(self):
        return self.registry.names()

    def _clean_result(self, result):
        if isinstance(result, Exception):
            return None

        return result