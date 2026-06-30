from typing import Optional

from pydantic import BaseModel


class PeerSnapshot(BaseModel):
    ticker: str
    company: Optional[str] = None
    industry: Optional[str] = None

    price: Optional[float] = None
    market_cap: Optional[float] = None

    pe_ratio: Optional[float] = None
    price_to_sales: Optional[float] = None
    price_to_book: Optional[float] = None

    revenue_growth: Optional[float] = None
    net_income_growth: Optional[float] = None

    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None

    return_on_equity: Optional[float] = None

    overall_score: Optional[float] = None