from app.models.fundamentals import CompanyFundamentals
from app.scoring.growth_score import GrowthScoreEngine


def test_growth_score_with_strong_growth():
    fundamentals = CompanyFundamentals(
        revenue_growth=0.20,
        gross_profit_growth=0.18,
        operating_income_growth=0.16,
        net_income_growth=0.22,
        eps_growth=0.19,
        free_cash_flow_growth=0.17,
    )

    engine = GrowthScoreEngine()
    result = engine.calculate(fundamentals)

    assert result["score"] == 100
    assert "6 available growth metrics" in result["explanation"]


def test_growth_score_with_no_data():
    fundamentals = CompanyFundamentals()

    engine = GrowthScoreEngine()
    result = engine.calculate(fundamentals)

    assert result["score"] == 0
    assert result["explanation"] == "No growth metrics available."