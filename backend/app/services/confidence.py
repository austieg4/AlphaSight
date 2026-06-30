class ConfidenceService:
    def calculate_company_profile_confidence(
        self,
        fmp_profile,
        finnhub_profile,
        sec_company,
    ):
        score = 0.0

        if fmp_profile:
            score += 0.3

        if finnhub_profile:
            score += 0.25

        if sec_company:
            score += 0.35

        if fmp_profile and finnhub_profile:
            fmp_name = (fmp_profile.get("companyName") or "").lower()
            finnhub_name = (finnhub_profile.get("name") or "").lower()

            if fmp_name and finnhub_name and fmp_name in finnhub_name:
                score += 0.1

        return min(score, 1.0)

    def calculate_price_confidence(self, fmp_profile, alpha_vantage_quote):
        if fmp_profile and alpha_vantage_quote:
            return 0.9

        if fmp_profile or alpha_vantage_quote:
            return 0.75

        return 0.0

    def calculate_macro_confidence(self, macro_snapshot):
        if not macro_snapshot:
            return 0.0

        available_series = [
            value for value in macro_snapshot.values()
            if value is not None
        ]

        return len(available_series) / len(macro_snapshot)