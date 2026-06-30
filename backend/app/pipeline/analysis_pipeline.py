from app.intelligence.investment_thesis import InvestmentThesisEngine
from app.intelligence.recommendation_engine import RecommendationEngine
from app.intelligence.risk_engine import RiskEngine
from app.pipeline.stages.peer_analysis_stage import PeerAnalysisStage
from app.services.market_data import MarketDataService


class AnalysisPipeline:
    """
    Executes the complete AlphaSight analysis workflow.
    """

    def __init__(self):
        self.market_data_service = MarketDataService()
        self.peer_analysis_stage = PeerAnalysisStage(self.market_data_service)
        self.thesis_engine = InvestmentThesisEngine()
        self.risk_engine = RiskEngine()
        self.recommendation_engine = RecommendationEngine()

    async def run(self, ticker: str):
        company = await self.market_data_service.get_company_overview(ticker)

        if company is None:
            return None

        company = await self.peer_analysis_stage.run(company)

        company.thesis = self.thesis_engine.build(company)
        company.risk = self.risk_engine.build(company)
        company.recommendation = self.recommendation_engine.build(company)

        return company