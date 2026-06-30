from app.intelligence.investment_thesis import InvestmentThesisEngine
from app.pipeline.stages.base_stage import AnalysisStage


class ThesisStage(AnalysisStage):
    """
    Builds the deterministic investment thesis.
    """

    def __init__(self):
        self.thesis_engine = InvestmentThesisEngine()

    async def run(self, company):
        company.thesis = self.thesis_engine.build(company)
        return company