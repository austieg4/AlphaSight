from typing import Optional

from pydantic import BaseModel


class PeerMetricComparison(BaseModel):
    metric: str
    company_value: float
    peer_average: float
    difference_percent: float
    assessment: str


class PeerAnalysis(BaseModel):
    pe_ratio: Optional[PeerMetricComparison] = None
    revenue_growth: Optional[PeerMetricComparison] = None
    gross_margin: Optional[PeerMetricComparison] = None
    operating_margin: Optional[PeerMetricComparison] = None
    return_on_equity: Optional[PeerMetricComparison] = None
    overall_score: Optional[PeerMetricComparison] = None
    peer_count: int
    status: str