from app.intelligence.investment_thesis import InvestmentThesisEngine
from app.intelligence.recommendation_engine import RecommendationEngine
from app.intelligence.risk_engine import RiskEngine
from app.models.peer_analysis import PeerAnalysis
from app.peer.peer_comparison import PeerComparisonEngine
from app.peer.peer_data_service import PeerDataService
from app.services.market_data import MarketDataService


class AnalysisPipeline:
    """
    Executes the complete AlphaSight analysis workflow.
    """

    def __init__(self):
        self.market_data_service = MarketDataService()
        self.peer_data_service = PeerDataService()
        self.peer_comparison = PeerComparisonEngine()
        self.thesis_engine = InvestmentThesisEngine()
        self.risk_engine = RiskEngine()
        self.recommendation_engine = RecommendationEngine()

    async def run(self, ticker: str):
        company = await self.market_data_service.get_company_overview(ticker)

        if company is None:
            return None

        company_snapshot = self.peer_data_service.build_snapshot(company)

        peer_snapshots = await self.peer_data_service.build_peer_snapshots(
            company.peers.peers,
            self.market_data_service,
        )

        company.peer_analysis = PeerAnalysis(
            pe_ratio=self.peer_comparison.compare_metric(
                company_snapshot,
                peer_snapshots,
                "pe_ratio",
            ),
            revenue_growth=self.peer_comparison.compare_metric(
                company_snapshot,
                peer_snapshots,
                "revenue_growth",
            ),
            gross_margin=self.peer_comparison.compare_metric(
                company_snapshot,
                peer_snapshots,
                "gross_margin",
            ),
            operating_margin=self.peer_comparison.compare_metric(
                company_snapshot,
                peer_snapshots,
                "operating_margin",
            ),
            return_on_equity=self.peer_comparison.compare_metric(
                company_snapshot,
                peer_snapshots,
                "return_on_equity",
            ),
            overall_score=self.peer_comparison.compare_metric(
                company_snapshot,
                peer_snapshots,
                "overall_score",
            ),
            peer_count=len(peer_snapshots),
            status="complete",
        )

        company.thesis = self.thesis_engine.build(company)
        company.risk = self.risk_engine.build(company)
        company.recommendation = self.recommendation_engine.build(company)

        return company