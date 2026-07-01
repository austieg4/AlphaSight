from app.services.analysis_service import AnalysisService
from app.pipeline.analysis_pipeline import AnalysisPipeline


def test_analysis_service_uses_pipeline():
    service = AnalysisService()

    assert isinstance(service.pipeline, AnalysisPipeline)