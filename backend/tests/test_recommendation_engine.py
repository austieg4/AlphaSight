from app.intelligence.recommendation_engine import RecommendationEngine
from app.models.recommendation import InvestmentRecommendation


class Category:
    def __init__(self, score):
        self.score = score


class Score:
    def __init__(self, overall_score):
        self.overall_score = overall_score
        self.categories = {
            "valuation": Category(80),
            "growth": Category(75),
            "profitability": Category(90),
            "financial_health": Category(80),
        }


class Thesis:
    rating = "Constructive"
    strengths = ["Strong profitability profile."]
    risks = ["P/E ratio is above peer average."]


class Risk:
    overall_risk = "Moderate"
    identified_risks = ["Revenue growth trails peer average."]
    mitigating_factors = ["Strong net margin helps offset risk."]


class Company:
    def __init__(self, overall_score):
        self.score = Score(overall_score)
        self.thesis = Thesis()
        self.risk = Risk()


def test_recommendation_watch_consider():
    company = Company(78)

    result = RecommendationEngine().build(company)

    assert isinstance(result, InvestmentRecommendation)
    assert result.action == "Watch / Consider"
    assert result.confidence == "Medium"
    assert result.status == "recommendation_engine_v3"


def test_recommendation_buy():
    company = Company(90)
    company.risk.overall_risk = "Low"

    result = RecommendationEngine().build(company)

    assert result.action == "Buy"
    assert result.confidence == "High"


def test_recommendation_avoid_when_risk_high():
    company = Company(90)
    company.risk.overall_risk = "High"

    result = RecommendationEngine().build(company)

    assert result.action == "Avoid / High Risk"
    assert result.confidence == "Low"