from app.models.recommendation import InvestmentRecommendation


class RecommendationEngine:
    def build(self, company):
        reasoning = []
        cautions = []

        score = company.score
        thesis = company.thesis
        risk = company.risk

        overall_score = score.overall_score if score else 0
        risk_level = risk.overall_risk if risk else "Unknown"

        if overall_score >= 85 and risk_level != "High":
            action = "Buy"
            confidence = "High"
        elif overall_score >= 70 and risk_level in ["Low", "Moderate"]:
            action = "Watch / Consider"
            confidence = "Medium"
        elif overall_score >= 55:
            action = "Hold / Neutral"
            confidence = "Medium"
        else:
            action = "Avoid / High Risk"
            confidence = "Low"

        if risk_level == "High":
            action = "Avoid / High Risk"
            confidence = "Low"

        if thesis:
            reasoning.append(
                f"Investment thesis is {thesis.rating.lower()}."
            )
            reasoning.extend(thesis.strengths)
            cautions.extend(thesis.risks)

        if risk:
            if risk.overall_risk == "Low":
                reasoning.append("Overall risk profile is low.")
            elif risk.overall_risk == "Moderate":
                cautions.append("Overall risk profile is moderate.")
            else:
                cautions.append("Overall risk profile is high.")

            cautions.extend(risk.identified_risks)
            reasoning.extend(risk.mitigating_factors)

        if score:
            profitability = score.categories.get("profitability")
            growth = score.categories.get("growth")
            valuation = score.categories.get("valuation")
            financial_health = score.categories.get("financial_health")

            if (
                profitability
                and profitability.score >= 90
                and "Strong profitability profile." not in reasoning
            ):
                reasoning.append("Exceptional profitability metrics.")

            if growth and growth.score >= 80:
                reasoning.append("Growth metrics are among the strongest in the model.")

            if valuation and valuation.score < 40:
                cautions.append("Valuation remains stretched.")

            if financial_health and financial_health.score < 50:
                cautions.append("Financial health should be monitored.")

        reasoning = list(dict.fromkeys(reasoning))
        cautions = list(dict.fromkeys(cautions))

        if not reasoning:
            reasoning.append("Recommendation generated from AlphaSight analysis.")

        if not cautions:
            cautions.append("No significant risks identified.")

        return InvestmentRecommendation(
            action=action,
            confidence=confidence,
            time_horizon="Long Term",
            reasoning=reasoning,
            cautions=cautions,
            status="recommendation_engine_v3",
        )