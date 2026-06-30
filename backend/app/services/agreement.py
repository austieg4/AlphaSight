from math import fabs

from app.models.agreement import PriceAgreement


class AgreementService:
    def calculate_price_agreement(
        self,
        fmp_profile,
        alpha_vantage_quote,
    ):
        if not fmp_profile or not alpha_vantage_quote:
            return PriceAgreement(
                score=0.0,
                difference_percent=0.0,
                providers=1,
                status="Insufficient Data",
            )

        try:
            fmp_price = float(fmp_profile["price"])
            alpha_price = float(alpha_vantage_quote["price"])
        except (TypeError, ValueError, KeyError):
            return PriceAgreement(
                score=0.0,
                difference_percent=0.0,
                providers=2,
                status="Invalid Data",
            )

        difference = fabs(fmp_price - alpha_price)
        average_price = (fmp_price + alpha_price) / 2

        if average_price == 0:
            agreement_score = 0.0
            difference_percent = 0.0
        else:
            difference_percent = (difference / average_price) * 100
            agreement_score = max(
                0.0,
                1 - (difference_percent / 100),
            )

        if agreement_score >= 0.999:
            status = "Excellent"
        elif agreement_score >= 0.995:
            status = "Very High"
        elif agreement_score >= 0.99:
            status = "High"
        elif agreement_score >= 0.97:
            status = "Medium"
        else:
            status = "Low"

        return PriceAgreement(
            score=round(agreement_score, 5),
            difference_percent=round(difference_percent, 5),
            providers=2,
            status=status,
        )