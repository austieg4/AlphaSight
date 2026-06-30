from app.intelligence.risk_engine import RiskEngine
from app.pipeline.stages.base_stage import AnalysisStage


class RiskStage(AnalysisStage):
    """
    Builds deterministic risk analysis.
    """

    def __init__(self):
        self.risk_engine = RiskEngine()

    async def run(self, company):
        company.risk = self.risk_engine.build(company)
        return company