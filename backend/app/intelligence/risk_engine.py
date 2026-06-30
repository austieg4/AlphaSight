from app.models.risk import RiskAnalysis


class RiskEngine:
    def build(self, company):
        risks = []
        mitigating_factors = []

        score = company.score
        peer_analysis = company.peer_analysis
        fundamentals = company.fundamentals
        agreement = company.agreement

        risk_points = 0

        if score:
            valuation = score.categories.get("valuation")
            financial_health = score.categories.get("financial_health")
            growth = score.categories.get("growth")
            source_agreement = score.categories.get("source_agreement")

            if valuation and valuation.score < 50:
                risk_points += 25
                risks.append("Valuation risk is elevated.")

            if financial_health and financial_health.score < 60:
                risk_points += 20
                risks.append("Financial health is below preferred levels.")

            if growth and growth.score < 50:
                risk_points += 15
                risks.append("Growth risk is elevated.")

            if source_agreement and source_agreement.score < 70:
                risk_points += 15
                risks.append("Provider agreement risk is elevated.")

        if fundamentals:
            if fundamentals.free_cash_flow_growth is not None and fundamentals.free_cash_flow_growth < 0:
                risk_points += 10
                risks.append("Free cash flow growth is negative.")

            if fundamentals.debt_to_equity is not None and fundamentals.debt_to_equity > 2:
                risk_points += 10
                risks.append("Debt-to-equity is elevated.")

            if fundamentals.current_ratio is not None and fundamentals.current_ratio < 1:
                risk_points += 10
                risks.append("Current ratio is below 1.0.")

            if fundamentals.net_margin is not None and fundamentals.net_margin > 0.20:
                mitigating_factors.append("Strong net margin helps offset risk.")

            if fundamentals.return_on_equity is not None and fundamentals.return_on_equity > 0.20:
                mitigating_factors.append("Strong return on equity helps offset risk.")

        if peer_analysis:
            if (
                peer_analysis.pe_ratio
                and peer_analysis.pe_ratio.assessment == "Above Peer Average"
            ):
                risk_points += 10
                risks.append("P/E ratio is above peer average.")

            if (
                peer_analysis.revenue_growth
                and peer_analysis.revenue_growth.assessment == "Below Peer Average"
            ):
                risk_points += 10
                risks.append("Revenue growth trails peer average.")

            if (
                peer_analysis.overall_score
                and peer_analysis.overall_score.assessment == "Above Peer Average"
            ):
                mitigating_factors.append("Overall score is above peer average.")

        if agreement and agreement.price.status in ["Insufficient Data", "Invalid Data"]:
            risk_points += 10
            risks.append("Price agreement is limited due to missing or invalid provider data.")

        risk_score = min(risk_points, 100)

        if risk_score >= 70:
            overall_risk = "High"
        elif risk_score >= 40:
            overall_risk = "Moderate"
        else:
            overall_risk = "Low"

        if not risks:
            risks.append("No major risks identified by current model.")

        if not mitigating_factors:
            mitigating_factors.append("No major mitigating factors identified by current model.")

        return RiskAnalysis(
            overall_risk=overall_risk,
            risk_score=risk_score,
            identified_risks=list(dict.fromkeys(risks)),
            mitigating_factors=list(dict.fromkeys(mitigating_factors)),
            status="risk_engine_v1",
        )