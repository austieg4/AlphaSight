from typing import Optional

from pydantic import BaseModel

from app.models.confidence import ConfidenceDetail
from app.models.fundamentals import CompanyFundamentals


class CompanyOverview(BaseModel):
    ticker: str
    company: Optional[str] = None
    price: Optional[float] = None
    market_cap: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    summary: Optional[str] = None
    fundamentals: Optional[CompanyFundamentals] = None
    peers: dict
    sources: dict[str, bool]
    confidence: dict[str, ConfidenceDetail]
    agreement: dict
    score: dict
    status: str