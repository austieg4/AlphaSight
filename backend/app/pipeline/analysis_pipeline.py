from app.pipeline.stages.peer_analysis_stage import PeerAnalysisStage
from app.pipeline.stages.recommendation_stage import RecommendationStage
from app.pipeline.stages.risk_stage import RiskStage
from app.pipeline.stages.thesis_stage import ThesisStage
from app.services.market_data import MarketDataService


class AnalysisPipeline:
    """
    Executes the complete AlphaSight analysis workflow.
    """

    def __init__(self):
        self.market_data_service = MarketDataService()

        self.stages = [
            PeerAnalysisStage(self.market_data_service),
            ThesisStage(),
            RiskStage(),
            RecommendationStage(),
        ]

    async def run(self, ticker: str):
        company = await self.market_data_service.get_company_overview(ticker)

        if company is None:
            return None

        for stage in self.stages:
            company = await stage.run(company)

        return company