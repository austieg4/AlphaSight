from app.models.agreement import Agreement


class AgreementBuilder:
    def __init__(self, agreement_service):
        self.agreement_service = agreement_service

    def build(
        self,
        fmp_profile,
        alpha_vantage_quote,
    ):
        return Agreement(
            price=self.agreement_service.calculate_price_agreement(
                fmp_profile,
                alpha_vantage_quote,
            )
        )