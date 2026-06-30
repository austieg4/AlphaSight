from app.pipeline.analysis_pipeline import AnalysisPipeline


class AnalysisService:
    """
    Entry point for AlphaSight analysis requests.
    """

    def __init__(self):
        self.pipeline = AnalysisPipeline()

    async def analyze(self, ticker: str):
        return await self.pipeline.run(ticker)