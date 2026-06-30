from app.models.recommendation import InvestmentRecommendation


class RecommendationEngine:
    def build(self, company):
        reasoning = []
        cautions = []

        score = company.score
        thesis = company.thesis
        peer_analysis = company.peer_analysis

        overall_score = score.overall_score if score else 0

        if overall_score >= 85:
            action = "Buy"
            confidence = "High"
        elif overall_score >= 70:
            action = "Watch / Consider"
            confidence = "Medium"
        elif overall_score >= 55:
            action = "Hold / Neutral"
            confidence = "Medium"
        else:
            action = "Avoid / High Risk"
            confidence = "Low"

        if thesis:
            if thesis.rating in ["Bullish", "Constructive"]:
                reasoning.append(
                    f"Investment thesis is {thesis.rating.lower()}."
                )

            for strength in thesis.strengths:
                reasoning.append(strength)

            for risk in thesis.risks:
                cautions.append(risk)

        if score:
            valuation = score.categories.get("valuation")
            growth = score.categories.get("growth")
            profitability = score.categories.get("profitability")
            financial_health = score.categories.get("financial_health")

            if profitability and profitability.score >= 80:
                reasoning.append("Profitability score is strong.")

            if growth and growth.score >= 70:
                reasoning.append("Growth score supports the recommendation.")

            if valuation and valuation.score < 50:
                cautions.append("Valuation score is weak.")

            if financial_health and financial_health.score < 60:
                cautions.append("Financial health score is below preferred levels.")

        if peer_analysis:
            if (
                peer_analysis.overall_score
                and peer_analysis.overall_score.assessment == "Above Peer Average"
            ):
                reasoning.append("Overall score is above peer average.")

            if (
                peer_analysis.pe_ratio
                and peer_analysis.pe_ratio.assessment == "Above Peer Average"
            ):
                cautions.append("Stock trades at a P/E premium to peers.")

            if (
                peer_analysis.revenue_growth
                and peer_analysis.revenue_growth.assessment == "Below Peer Average"
            ):
                cautions.append("Revenue growth trails peer average.")

        reasoning = list(dict.fromkeys(reasoning))
        cautions = list(dict.fromkeys(cautions))

        if not reasoning:
            reasoning.append("Recommendation is based on AlphaSight scoring output.")

        if not cautions:
            cautions.append("No major cautions identified by current model.")

        return InvestmentRecommendation(
            action=action,
            confidence=confidence,
            time_horizon="Long Term",
            reasoning=reasoning,
            cautions=cautions,
            status="recommendation_engine_v1",
        )