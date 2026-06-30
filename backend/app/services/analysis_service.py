from app.peer.peer_data_service import PeerDataService
from app.services.market_data import MarketDataService


class AnalysisService:
    """
    Coordinates the complete AlphaSight analysis workflow.
    """

    def __init__(self):
        self.market_data_service = MarketDataService()
        self.peer_data_service = PeerDataService()

    async def analyze(self, ticker: str):
        company = await self.market_data_service.get_company_overview(ticker)

        if company is None:
            return None

        peer_snapshots = await self.peer_data_service.build_peer_snapshots(
            company.peers.peers,
            self.market_data_service,
        )

        # Temporary: store peer snapshot count inside peers status path later.
        # Next step will add a typed PeerAnalysis model.
        company.peers.status = f"dynamic_peer_snapshots_v1:{len(peer_snapshots)}"

        return company