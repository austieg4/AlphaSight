from app.peer.peer_data_service import PeerDataService
from app.services.market_data import MarketDataService


class AnalysisService:
    """
    Coordinates the complete AlphaSight analysis workflow.

    This service is intentionally lightweight. It orchestrates
    the various components without containing business logic.
    """

    def __init__(self):
        self.market_data_service = MarketDataService()
        self.peer_data_service = PeerDataService()

    async def analyze(self, ticker: str):
        """
        Build a complete company analysis.
        """

        company = await self.market_data_service.get_company_overview(ticker)

        if company is None:
            return None

        # Future:
        #
        # peer_snapshots =
        #     await self.peer_data_service.build_peer_snapshots(...)
        #
        # peer_analysis =
        #     PeerComparisonEngine(...)
        #
        # company.peer_analysis = peer_analysis

        return company