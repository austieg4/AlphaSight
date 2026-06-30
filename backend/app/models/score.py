from pydantic import BaseModel


class ScoreCategory(BaseModel):
    score: float
    explanation: str


class AlphaSightScore(BaseModel):
    overall_score: float
    max_score: int
    status: str
    categories: dict[str, ScoreCategory]