class ConfidenceBuilder:
    def __init__(self, confidence_service):
        self.confidence_service = confidence_service

    def build(
        self,
        fmp_profile,
        finnhub_profile,
        sec_company,
        alpha_vantage_quote,
        macro_snapshot,
    ):
        return {
            "company_profile": (
                self.confidence_service.calculate_company_profile_confidence(
                    fmp_profile,
                    finnhub_profile,
                    sec_company,
                )
            ),
            "price": (
                self.confidence_service.calculate_price_confidence(
                    fmp_profile,
                    alpha_vantage_quote,
                )
            ),
            "macro_context": (
                self.confidence_service.calculate_macro_confidence(
                    macro_snapshot,
                )
            ),
        }