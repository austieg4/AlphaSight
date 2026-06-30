class OverallScoreEngine:
    def calculate_score(self, company_overview):
        score = 0

        company_confidence = company_overview.confidence.get("company_profile")
        price_confidence = company_overview.confidence.get("price")
        macro_confidence = company_overview.confidence.get("macro_context")

        price_agreement = company_overview.agreement.get("price")

        if company_confidence:
            score += company_confidence.score * 30

        if price_confidence:
            score += price_confidence.score * 20

        if macro_confidence:
            score += macro_confidence.score * 20

        if price_agreement:
            score += price_agreement.get("score", 0) * 30

        return {
            "overall_score": round(score, 2),
            "max_score": 100,
            "status": self._score_status(score),
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