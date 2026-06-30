from app.models.thesis import InvestmentThesis


class InvestmentThesisEngine:
    def build(self, company):
        strengths = []
        risks = []

        score = company.score
        peer_analysis = company.peer_analysis

        overall_score = score.overall_score if score else 0

        if overall_score >= 85:
            rating = "Bullish"
        elif overall_score >= 70:
            rating = "Constructive"
        elif overall_score >= 55:
            rating = "Neutral"
        else:
            rating = "Cautious"

        if score:
            profitability = score.categories.get("profitability")
            growth = score.categories.get("growth")
            valuation = score.categories.get("valuation")
            financial_health = score.categories.get("financial_health")

            if profitability and profitability.score >= 80:
                strengths.append("Strong profitability profile.")

            if growth and growth.score >= 70:
                strengths.append("Healthy growth fundamentals.")

            if financial_health and financial_health.score >= 70:
                strengths.append("Solid financial health.")

            if valuation and valuation.score < 50:
                risks.append("Valuation appears elevated relative to scoring thresholds.")

            if growth and growth.score < 50:
                risks.append("Growth profile appears weak or inconsistent.")

            if financial_health and financial_health.score < 60:
                risks.append("Financial health score is below preferred levels.")

        if peer_analysis:
            if (
                peer_analysis.return_on_equity
                and peer_analysis.return_on_equity.assessment == "Above Peer Average"
            ):
                strengths.append("Return on equity is above peer average.")

            if (
                peer_analysis.overall_score
                and peer_analysis.overall_score.assessment == "Above Peer Average"
            ):
                strengths.append("Overall AlphaSight score is above peer average.")

            if (
                peer_analysis.pe_ratio
                and peer_analysis.pe_ratio.assessment == "Above Peer Average"
            ):
                risks.append("P/E ratio is above peer average.")

            if (
                peer_analysis.revenue_growth
                and peer_analysis.revenue_growth.assessment == "Below Peer Average"
            ):
                risks.append("Revenue growth is below peer average.")

        if not strengths:
            strengths.append("No major strengths identified from current scoring model.")

        if not risks:
            risks.append("No major risks identified from current scoring model.")

        summary = (
            f"{company.company or company.ticker} receives a {rating} rating "
            f"with an AlphaSight score of {overall_score} out of 100. "
            "This thesis is generated from deterministic scoring, peer analysis, "
            "provider confidence, and normalized fundamentals."
        )

        return InvestmentThesis(
            rating=rating,
            summary=summary,
            strengths=strengths,
            risks=risks,
            status="investment_thesis_v1",
        )