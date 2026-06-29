from typing import Optional

from pydantic import BaseModel


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
    confidence: dict[str, float]
    status: str