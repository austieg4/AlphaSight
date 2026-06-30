from pydantic import BaseModel


class ConfidenceDetail(BaseModel):
    score: float
    level: str
    explanation: str