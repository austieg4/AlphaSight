from app.models.confidence import ConfidenceDetail


class ConfidenceService:
    def calculate_company_profile_confidence(
        self,
        fmp_profile,
        finnhub_profile,
        sec_company,
    ):
        score = 0.0

        if fmp_profile:
            score += 0.30

        if finnhub_profile:
            score += 0.25

        if sec_company:
            score += 0.35

        if fmp_profile and finnhub_profile:
            fmp_name = (fmp_profile.get("companyName") or "").lower()
            finnhub_name = (finnhub_profile.get("name") or "").lower()

            if fmp_name and finnhub_name and fmp_name in finnhub_name:
                score += 0.10

        score = min(score, 1.0)

        if score >= 0.95:
            level = "Very High"
        elif score >= 0.85:
            level = "High"
        elif score >= 0.70:
            level = "Medium"
        else:
            level = "Low"

        return ConfidenceDetail(
            score=score,
            level=level,
            explanation=(
                "Calculated from Financial Modeling Prep, Finnhub, "
                "and SEC EDGAR agreement."
            ),
        )

    def calculate_price_confidence(self, fmp_profile, alpha_vantage_quote):
        if fmp_profile and alpha_vantage_quote:
            score = 0.90
            level = "High"
            explanation = (
                "Price confirmed by Financial Modeling Prep "
                "and Alpha Vantage."
            )

        elif fmp_profile or alpha_vantage_quote:
            score = 0.75
            level = "Medium"
            explanation = "Price available from one provider."

        else:
            score = 0.0
            level = "Unavailable"
            explanation = "No price data available."

        return ConfidenceDetail(
            score=score,
            level=level,
            explanation=explanation,
        )

    def calculate_macro_confidence(self, macro_snapshot):
        if not macro_snapshot:
            return ConfidenceDetail(
                score=0.0,
                level="Unavailable",
                explanation="No macroeconomic data available.",
            )

        available = sum(
            value is not None
            for value in macro_snapshot.values()
        )

        score = available / len(macro_snapshot)

        if score == 1.0:
            level = "Very High"
        elif score >= 0.75:
            level = "High"
        elif score >= 0.5:
            level = "Medium"
        else:
            level = "Low"

        return ConfidenceDetail(
            score=score,
            level=level,
            explanation=f"{available} of {len(macro_snapshot)} FRED indicators available.",
        )