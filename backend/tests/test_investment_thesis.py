from app.intelligence.investment_thesis import InvestmentThesisEngine
from app.models.company import CompanyOverview
from app.models.peer import PeerGroup
from app.models.peer_analysis import PeerAnalysis, PeerMetricComparison
from app.models.score import AlphaSightScore, ScoreCategory
from app.models.agreement import Agreement, PriceAgreement


def build_company(score_value=78.0):
    return CompanyOverview(
        ticker="AAPL",
        company="Apple Inc.",
        peers=PeerGroup(
            ticker="AAPL",
            peers=["MSFT"],
            peer_count=1,
            status="typed_peer_group_v1",
        ),
        peer_analysis=PeerAnalysis(
            return_on_equity=PeerMetricComparison(
                metric="return_on_equity",
                company_value=1.4,
                peer_average=0.3,
                difference_percent=350,
                assessment="Above Peer Average",
            ),
            overall_score=PeerMetricComparison(
                metric="overall_score",
                company_value=78,
                peer_average=60,
                difference_percent=30,
                assessment="Above Peer Average",
            ),
            pe_ratio=PeerMetricComparison(
                metric="pe_ratio",
                company_value=35,
                peer_average=25,
                difference_percent=40,
                assessment="Above Peer Average",
            ),
            peer_count=1,
            status="complete",
        ),
        sources={},
        confidence={},
        agreement=Agreement(
            price=PriceAgreement(
                score=1.0,
                difference_percent=0.0,
                providers=2,
                status="Excellent",
            )
        ),
        score=AlphaSightScore(
            overall_score=score_value,
            max_score=100,
            status="Good",
            categories={
                "profitability": ScoreCategory(
                    score=90,
                    explanation="Strong profitability.",
                ),
                "growth": ScoreCategory(
                    score=60,
                    explanation="Moderate growth.",
                ),
                "valuation": ScoreCategory(
                    score=45,
                    explanation="Expensive valuation.",
                ),
                "financial_health": ScoreCategory(
                    score=65,
                    explanation="Acceptable health.",
                ),
            },
        ),
        status="test",
    )


def test_investment_thesis_constructive_rating():
    company = build_company(78.0)

    thesis = InvestmentThesisEngine().build(company)

    assert thesis.rating == "Constructive"
    assert thesis.status == "investment_thesis_v1"
    assert "Strong profitability profile." in thesis.strengths
    assert "P/E ratio is above peer average." in thesis.risks


def test_investment_thesis_bullish_rating():
    company = build_company(90.0)

    thesis = InvestmentThesisEngine().build(company)

    assert thesis.rating == "Bullish"