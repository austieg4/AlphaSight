class GrowthScoreEngine:
    def calculate(self, fundamentals):
        if not fundamentals:
            return {"score": 0, "explanation": "No growth fundamentals available."}

        score = 0
        checks = 0

        growth_metrics = [
            fundamentals.revenue_growth,
            fundamentals.gross_profit_growth,
            fundamentals.operating_income_growth,
            fundamentals.net_income_growth,
            fundamentals.eps_growth,
            fundamentals.free_cash_flow_growth,
        ]

        for metric in growth_metrics:
            if metric is None:
                continue

            checks += 1

            if metric > 0.15:
                score += 100
            elif metric > 0.08:
                score += 75
            elif metric > 0.03:
                score += 50
            elif metric >= 0:
                score += 25
            else:
                score += 0

        if checks == 0:
            return {"score": 0, "explanation": "No growth metrics available."}

        return {
            "score": round(score / checks, 2),
            "explanation": f"Growth score based on {checks} available growth metrics.",
        }