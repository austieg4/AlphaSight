from pydantic import BaseModel


class RiskAnalysis(BaseModel):
    overall_risk: str
    risk_score: float
    identified_risks: list[str]
    mitigating_factors: list[str]
    status: str