from app.intelligence.risk_engine import RiskEngine
from app.models.risk import RiskAnalysis


class Category:
    def __init__(self, score):
        self.score = score


class Score:
    def __init__(
        self,
        overall_score,
        valuation,
        growth,
        profitability,
        financial_health,
        source_agreement,
    ):
        self.overall_score = overall_score
        self.categories = {
            "valuation": Category(valuation),
            "growth": Category(growth),
            "profitability": Category(profitability),
            "financial_health": Category(financial_health),
            "source_agreement": Category(source_agreement),
        }


class AgreementPrice:
    def __init__(self, status):
        self.status = status


class Agreement:
    def __init__(self, status):
        self.price = AgreementPrice(status)


class PeerMetric:
    def __init__(self, assessment):
        self.assessment = assessment


class PeerAnalysis:
    def __init__(self):
        self.pe_ratio = PeerMetric("Above Peer Average")
        self.revenue_growth = PeerMetric("Below Peer Average")
        self.overall_score = PeerMetric("Above Peer Average")


class Fundamentals:
    def __init__(
        self,
        free_cash_flow_growth,
        debt_to_equity,
        current_ratio,
        net_margin,
        return_on_equity,
    ):
        self.free_cash_flow_growth = free_cash_flow_growth
        self.debt_to_equity = debt_to_equity
        self.current_ratio = current_ratio
        self.net_margin = net_margin
        self.return_on_equity = return_on_equity


class Company:
    def __init__(
        self,
        overall_score,
        valuation,
        growth,
        profitability,
        financial_health,
        source_agreement,
        agreement_status,
        fundamentals,
    ):
        self.score = Score(
            overall_score,
            valuation,
            growth,
            profitability,
            financial_health,
            source_agreement,
        )
        self.agreement = Agreement(agreement_status)
        self.peer_analysis = PeerAnalysis()
        self.fundamentals = fundamentals


def test_high_risk_company():
    company = Company(
        overall_score=35,
        valuation=20,
        growth=20,
        profitability=40,
        financial_health=30,
        source_agreement=20,
        agreement_status="Insufficient Data",
        fundamentals=Fundamentals(
            free_cash_flow_growth=-0.10,
            debt_to_equity=3.0,
            current_ratio=0.8,
            net_margin=0.05,
            return_on_equity=0.05,
        ),
    )

    result = RiskEngine().build(company)

    assert isinstance(result, RiskAnalysis)
    assert result.overall_risk == "High"
    assert result.risk_score >= 70


def test_low_risk_company():
    company = Company(
        overall_score=92,
        valuation=90,
        growth=92,
        profitability=95,
        financial_health=95,
        source_agreement=100,
        agreement_status="Excellent",
        fundamentals=Fundamentals(
            free_cash_flow_growth=0.15,
            debt_to_equity=0.4,
            current_ratio=2.0,
            net_margin=0.28,
            return_on_equity=0.42,
        ),
    )

    result = RiskEngine().build(company)

    assert isinstance(result, RiskAnalysis)
    assert result.overall_risk == "Low"
    assert result.risk_score <= 35