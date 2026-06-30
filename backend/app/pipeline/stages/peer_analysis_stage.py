from app.models.peer_analysis import PeerAnalysis
from app.peer.peer_comparison import PeerComparisonEngine
from app.peer.peer_data_service import PeerDataService
from app.pipeline.stages.base_stage import AnalysisStage


class PeerAnalysisStage(AnalysisStage):
    """
    Builds peer snapshots and peer comparison analysis.
    """

    def __init__(self, market_data_service):
        self.market_data_service = market_data_service
        self.peer_data_service = PeerDataService()
        self.peer_comparison = PeerComparisonEngine()

    async def run(self, company):
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

        return company