class ProfitabilityScoreEngine:
    def calculate(self, fundamentals):
        if not fundamentals:
            return {"score": 0, "explanation": "No profitability fundamentals available."}

        score = 0
        checks = 0

        if fundamentals.gross_margin is not None:
            checks += 1
            if fundamentals.gross_margin > 0.5:
                score += 100
            elif fundamentals.gross_margin > 0.35:
                score += 75
            elif fundamentals.gross_margin > 0.2:
                score += 50
            else:
                score += 25

        if fundamentals.net_margin is not None:
            checks += 1
            if fundamentals.net_margin > 0.2:
                score += 100
            elif fundamentals.net_margin > 0.1:
                score += 75
            elif fundamentals.net_margin > 0.05:
                score += 50
            else:
                score += 25

        if fundamentals.return_on_equity is not None:
            checks += 1
            if fundamentals.return_on_equity > 0.25:
                score += 100
            elif fundamentals.return_on_equity > 0.15:
                score += 75
            elif fundamentals.return_on_equity > 0.08:
                score += 50
            else:
                score += 25

        if checks == 0:
            return {"score": 0, "explanation": "No profitability metrics available."}

        return {
            "score": round(score / checks, 2),
            "explanation": f"Profitability score based on {checks} available profitability metrics.",
        }