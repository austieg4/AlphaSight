class ValuationScoreEngine:
    def calculate(self, fundamentals):
        if not fundamentals:
            return {"score": 0, "explanation": "No valuation fundamentals available."}

        score = 0
        checks = 0

        if fundamentals.pe_ratio is not None:
            checks += 1
            if fundamentals.pe_ratio < 20:
                score += 100
            elif fundamentals.pe_ratio < 30:
                score += 75
            elif fundamentals.pe_ratio < 45:
                score += 50
            else:
                score += 25

        if fundamentals.price_to_sales is not None:
            checks += 1
            if fundamentals.price_to_sales < 3:
                score += 100
            elif fundamentals.price_to_sales < 7:
                score += 75
            elif fundamentals.price_to_sales < 12:
                score += 50
            else:
                score += 25

        if fundamentals.price_to_book is not None:
            checks += 1
            if fundamentals.price_to_book < 3:
                score += 100
            elif fundamentals.price_to_book < 8:
                score += 75
            elif fundamentals.price_to_book < 15:
                score += 50
            else:
                score += 25

        if checks == 0:
            return {"score": 0, "explanation": "No valuation metrics available."}

        return {
            "score": round(score / checks, 2),
            "explanation": f"Valuation score based on {checks} available valuation metrics.",
        }