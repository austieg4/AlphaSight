from pydantic import BaseModel


class InvestmentThesis(BaseModel):
    rating: str
    summary: str
    strengths: list[str]
    risks: list[str]
    status: str