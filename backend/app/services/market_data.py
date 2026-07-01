from app.builders.agreement_builder import AgreementBuilder
from app.builders.company_overview_builder import CompanyOverviewBuilder
from app.builders.confidence_builder import ConfidenceBuilder
from app.builders.fundamentals_builder import FundamentalsBuilder
from app.intelligence.peer_intelligence import PeerIntelligence
from app.providers.provider_manager import ProviderManager
from app.scoring.overall_score import OverallScoreEngine
from app.services.agreement import AgreementService
from app.services.confidence import ConfidenceService


class MarketDataService:
    def __init__(self):
        self.provider_manager = ProviderManager()

        self.confidence_service = ConfidenceService()
        self.agreement_service = AgreementService()

        self.fundamentals_builder = FundamentalsBuilder()
        self.company_overview_builder = CompanyOverviewBuilder()
        self.confidence_builder = ConfidenceBuilder(self.confidence_service)
        self.agreement_builder = AgreementBuilder(self.agreement_service)

        self.peer_intelligence = PeerIntelligence()
        self.score_engine = OverallScoreEngine()

    async def get_company_overview(self, ticker: str):
        clean_ticker = ticker.upper()

        provider_data = await self.provider_manager.fetch_company_data(clean_ticker)

        fmp_profile = provider_data["fmp_profile"]
        fmp_key_metrics = provider_data["fmp_key_metrics"]
        fmp_ratios = provider_data["fmp_ratios"]
        fmp_growth = provider_data["fmp_growth"]
        finnhub_profile = provider_data["finnhub_profile"]
        alpha_vantage_quote = provider_data["alpha_vantage_quote"]
        sec_company = provider_data["sec_company"]
        macro_snapshot = provider_data["macro_snapshot"]

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

        confidence = self.confidence_builder.build(
            fmp_profile=fmp_profile,
            finnhub_profile=finnhub_profile,
            sec_company=sec_company,
            alpha_vantage_quote=alpha_vantage_quote,
            macro_snapshot=macro_snapshot,
        )

        agreement = self.agreement_builder.build(
            fmp_profile=fmp_profile,
            alpha_vantage_quote=alpha_vantage_quote,
        )

        peers = self.peer_intelligence.get_peer_summary(clean_ticker)

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
            peers=peers,
        )

        company_overview.score = self.score_engine.calculate_score(company_overview)

        return company_overview
    