import asyncio

from app.models.company import CompanyOverview
from app.models.fundamentals import CompanyFundamentals
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
        self.confidence_service = ConfidenceService()
        self.agreement_service = AgreementService()
        self.score_engine = OverallScoreEngine()

    async def get_company_overview(self, ticker: str):
        clean_ticker = ticker.upper()

        results = await asyncio.gather(
            self.fmp_provider.get_company_profile(clean_ticker),
            self.fmp_provider.get_key_metrics_ttm(clean_ticker),
            self.fmp_provider.get_ratios_ttm(clean_ticker),
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

        fundamentals = self._build_fundamentals(
            fmp_key_metrics,
            fmp_ratios,
        )

        price_agreement = self.agreement_service.calculate_price_agreement(
            fmp_profile,
            alpha_vantage_quote,
        )

        company_overview = CompanyOverview(
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
            fundamentals=fundamentals,
            sources={
                "fmp_profile": fmp_profile is not None,
                "fmp_key_metrics_ttm": fmp_key_metrics is not None,
                "fmp_ratios_ttm": fmp_ratios is not None,
                "finnhub_profile": finnhub_profile is not None,
                "alpha_vantage_quote": alpha_vantage_quote is not None,
                "sec_company": sec_company is not None,
                "fred_macro": macro_snapshot is not None,
            },
            confidence={
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
            },
            agreement={
                "price": price_agreement,
            },
            score={},
            status="investment_scoring_engine_v1",
        )

        company_overview.score = self.score_engine.calculate_score(company_overview)

        return company_overview

    def _build_fundamentals(self, key_metrics, ratios):
        if key_metrics is None and ratios is None:
            return None

        key_metrics = key_metrics or {}
        ratios = ratios or {}

        return CompanyFundamentals(
            pe_ratio=key_metrics.get("peRatioTTM"),
            price_to_sales=key_metrics.get("priceToSalesRatioTTM"),
            price_to_book=key_metrics.get("pbRatioTTM"),
            ev_to_ebitda=key_metrics.get("enterpriseValueOverEBITDATTM"),
            current_ratio=ratios.get("currentRatioTTM"),
            debt_to_equity=ratios.get("debtEquityRatioTTM"),
            gross_margin=ratios.get("grossProfitMarginTTM"),
            operating_margin=ratios.get("operatingProfitMarginTTM"),
            net_margin=ratios.get("netProfitMarginTTM"),
            return_on_equity=ratios.get("returnOnEquityTTM"),
            return_on_assets=ratios.get("returnOnAssetsTTM"),
            revenue_per_share=key_metrics.get("revenuePerShareTTM"),
            net_income_per_share=key_metrics.get("netIncomePerShareTTM"),
            free_cash_flow_per_share=key_metrics.get("freeCashFlowPerShareTTM"),
            cash_per_share=key_metrics.get("cashPerShareTTM"),
            book_value_per_share=key_metrics.get("bookValuePerShareTTM"),
        )