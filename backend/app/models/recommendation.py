from pydantic import BaseModel


class InvestmentRecommendation(BaseModel):
    action: str
    confidence: str
    time_horizon: str
    reasoning: list[str]
    cautions: list[str]
    status: str