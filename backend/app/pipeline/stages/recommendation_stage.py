from app.intelligence.recommendation_engine import RecommendationEngine
from app.pipeline.stages.base_stage import AnalysisStage


class RecommendationStage(AnalysisStage):
    """
    Builds the final investment recommendation.
    """

    def __init__(self):
        self.recommendation_engine = RecommendationEngine()

    async def run(self, company):
        company.recommendation = self.recommendation_engine.build(company)
        return company