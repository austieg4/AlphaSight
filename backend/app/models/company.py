from typing import Optional

from pydantic import BaseModel

from app.models.confidence import ConfidenceDetail


class CompanyOverview(BaseModel):
    ticker: str
    company: Optional[str] = None
    price: Optional[float] = None
    market_cap: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    summary: Optional[str] = None
    sources: dict[str, bool]
    confidence: dict[str, ConfidenceDetail]
    agreement: dict
    status: str