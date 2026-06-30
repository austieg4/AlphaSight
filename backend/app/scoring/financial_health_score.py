class FinancialHealthScoreEngine:
    def calculate(self, fundamentals):
        if not fundamentals:
            return {"score": 0, "explanation": "No financial health fundamentals available."}

        score = 0
        checks = 0

        if fundamentals.current_ratio is not None:
            checks += 1
            if fundamentals.current_ratio > 2:
                score += 100
            elif fundamentals.current_ratio > 1.5:
                score += 75
            elif fundamentals.current_ratio > 1:
                score += 50
            else:
                score += 25

        if fundamentals.debt_to_equity is not None:
            checks += 1
            if fundamentals.debt_to_equity < 0.5:
                score += 100
            elif fundamentals.debt_to_equity < 1:
                score += 75
            elif fundamentals.debt_to_equity < 2:
                score += 50
            else:
                score += 25

        if checks == 0:
            return {"score": 0, "explanation": "No financial health metrics available."}

        return {
            "score": round(score / checks, 2),
            "explanation": f"Financial health score based on {checks} available balance sheet metrics.",
        }