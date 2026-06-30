from app.scoring.financial_health_score import FinancialHealthScoreEngine
from app.scoring.growth_score import GrowthScoreEngine
from app.scoring.profitability_score import ProfitabilityScoreEngine
from app.scoring.valuation_score import ValuationScoreEngine


class OverallScoreEngine:
    def __init__(self):
        self.valuation_engine = ValuationScoreEngine()
        self.growth_engine = GrowthScoreEngine()
        self.profitability_engine = ProfitabilityScoreEngine()
        self.financial_health_engine = FinancialHealthScoreEngine()

    def calculate_score(self, company_overview):
        data_quality = self._score_data_quality(company_overview)
        source_agreement = self._score_source_agreement(company_overview)
        macro_context = self._score_macro_context(company_overview)
        company_identity = self._score_company_identity(company_overview)

        valuation = self.valuation_engine.calculate(
            company_overview.fundamentals
        )

        growth = self.growth_engine.calculate(
            company_overview.fundamentals
        )

        profitability = self.profitability_engine.calculate(
            company_overview.fundamentals
        )

        financial_health = self.financial_health_engine.calculate(
            company_overview.fundamentals
        )

        overall_score = (
            valuation["score"] * 0.20
            + growth["score"] * 0.20
            + profitability["score"] * 0.20
            + financial_health["score"] * 0.15
            + data_quality["score"] * 0.10
            + source_agreement["score"] * 0.05
            + macro_context["score"] * 0.05
            + company_identity["score"] * 0.05
        )

        return {
            "overall_score": round(overall_score, 2),
            "max_score": 100,
            "status": self._score_status(overall_score),
            "categories": {
                "valuation": valuation,
                "growth": growth,
                "profitability": profitability,
                "financial_health": financial_health,
                "data_quality": data_quality,
                "source_agreement": source_agreement,
                "macro_context": macro_context,
                "company_identity": company_identity,
            },
        }

    def _score_data_quality(self, company_overview):
        sources = company_overview.sources

        active_sources = sum(
            1 for active in sources.values() if active
        )

        total_sources = len(sources)

        score = (
            (active_sources / total_sources) * 100
            if total_sources
            else 0
        )

        return {
            "score": round(score, 2),
            "explanation": (
                f"{active_sources} of {total_sources} "
                "data sources responded."
            ),
        }

    def _score_source_agreement(self, company_overview):
        agreement = company_overview.agreement.get("price", {})

        return {
            "score": agreement.get("score", 0) * 100,
            "explanation": (
                f"Price agreement status: "
                f"{agreement.get('status', 'Unknown')}."
            ),
        }

    def _score_macro_context(self, company_overview):
        macro = company_overview.confidence.get("macro_context")

        if not macro:
            return {
                "score": 0,
                "explanation": "No macroeconomic context available.",
            }

        return {
            "score": macro.score * 100,
            "explanation": macro.explanation,
        }

    def _score_company_identity(self, company_overview):
        identity = company_overview.confidence.get(
            "company_profile"
        )

        if not identity:
            return {
                "score": 0,
                "explanation": "Company identity unavailable.",
            }

        return {
            "score": identity.score * 100,
            "explanation": identity.explanation,
        }

    def _score_status(self, score):
        if score >= 90:
            return "Excellent"

        if score >= 80:
            return "Strong"

        if score >= 70:
            return "Good"

        if score >= 60:
            return "Moderate"

        return "Weak"