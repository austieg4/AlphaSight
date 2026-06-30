from typing import Optional

from pydantic import BaseModel

from app.models.agreement import Agreement
from app.models.confidence import ConfidenceDetail
from app.models.fundamentals import CompanyFundamentals
from app.models.peer import PeerGroup
from app.models.peer_analysis import PeerAnalysis
from app.models.score import AlphaSightScore
from app.models.thesis import InvestmentThesis


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
    peers: PeerGroup
    peer_analysis: Optional[PeerAnalysis] = None
    thesis: Optional[InvestmentThesis] = None
    sources: dict[str, bool]
    confidence: dict[str, ConfidenceDetail]
    agreement: Agreement
    score: Optional[AlphaSightScore] = None
    status: str