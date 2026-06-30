import asyncio

from app.builders.company_overview_builder import CompanyOverviewBuilder
from app.builders.fundamentals_builder import FundamentalsBuilder
from app.providers.alpha_vantage import AlphaVantageProvider
from app.providers.finnhub import FinnhubProvider
from app.providers.fmp import FMPProvider
from app.providers.fred import FREDProvider
from app.providers.sec_edgar import SECEdgarProvider
from app.scoring.overall_score import OverallScoreEngine
from app.services.agreement import AgreementService
from app.services.confidence import ConfidenceService


class MarketDataService:
    def __init__(self):
        self.fmp_provider = FMPProvider()
        self.finnhub_provider = FinnhubProvider()
        self.alpha_vantage_provider = AlphaVantageProvider()
        self.sec_provider = SECEdgarProvider()
        self.fred_provider = FREDProvider()
        self.fundamentals_builder = FundamentalsBuilder()
        self.company_overview_builder = CompanyOverviewBuilder()
        self.confidence_service = ConfidenceService()
        self.agreement_service = AgreementService()
        self.score_engine = OverallScoreEngine()

    async def get_company_overview(self, ticker: str):
        clean_ticker = ticker.upper()

        results = await asyncio.gather(
            self.fmp_provider.get_company_profile(clean_ticker),
            self.fmp_provider.get_key_metrics_ttm(clean_ticker),
            self.fmp_provider.get_ratios_ttm(clean_ticker),
            self.fmp_provider.get_financial_growth(clean_ticker),
            self.finnhub_provider.get_company_profile(clean_ticker),
            self.alpha_vantage_provider.get_global_quote(clean_ticker),
            self.sec_provider.get_company(clean_ticker),
            self.fred_provider.get_macro_snapshot(),
            return_exceptions=True,
        )

        (
            fmp_profile,
            fmp_key_metrics,
            fmp_ratios,
            fmp_growth,
            finnhub_profile,
            alpha_vantage_quote,
            sec_company,
            macro_snapshot,
        ) = [
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

        fundamentals = self.fundamentals_builder.build(
            fmp_key_metrics,
            fmp_ratios,
            fmp_growth,
        )

        confidence = {
            "company_profile": self.confidence_service.calculate_company_profile_confidence(
                fmp_profile,
                finnhub_profile,
                sec_company,
            ),
            "price": self.confidence_service.calculate_price_confidence(
                fmp_profile,
                alpha_vantage_quote,
            ),
            "macro_context": self.confidence_service.calculate_macro_confidence(
                macro_snapshot,
            ),
        }

        agreement = {
            "price": self.agreement_service.calculate_price_agreement(
                fmp_profile,
                alpha_vantage_quote,
            ),
        }

        company_overview = self.company_overview_builder.build(
            ticker=clean_ticker,
            fmp_profile=fmp_profile,
            finnhub_profile=finnhub_profile,
            alpha_vantage_quote=alpha_vantage_quote,
            sec_company=sec_company,
            fundamentals=fundamentals,
            macro_snapshot=macro_snapshot,
            confidence=confidence,
            agreement=agreement,
        )

        company_overview.score = self.score_engine.calculate_score(company_overview)

        return company_overview