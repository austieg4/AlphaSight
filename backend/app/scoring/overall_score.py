class OverallScoreEngine:
    def calculate_score(self, company_overview):
        data_quality = self._score_data_quality(company_overview)
        source_agreement = self._score_source_agreement(company_overview)
        macro_context = self._score_macro_context(company_overview)
        company_identity = self._score_company_identity(company_overview)

        overall_score = (
            data_quality["score"] * 0.30
            + source_agreement["score"] * 0.30
            + macro_context["score"] * 0.20
            + company_identity["score"] * 0.20
        )

        return {
            "overall_score": round(overall_score, 2),
            "max_score": 100,
            "status": self._score_status(overall_score),
            "categories": {
                "data_quality": data_quality,
                "source_agreement": source_agreement,
                "macro_context": macro_context,
                "company_identity": company_identity,
            },
        }

    def _score_data_quality(self, company_overview):
        sources = company_overview.sources
        active_sources = sum(1 for active in sources.values() if active)
        total_sources = len(sources)

        score = (active_sources / total_sources) * 100 if total_sources else 0

        return {
            "score": round(score, 2),
            "explanation": f"{active_sources} of {total_sources} data sources responded.",
        }

    def _score_source_agreement(self, company_overview):
        price_agreement = company_overview.agreement.get("price", {})
        score = price_agreement.get("score", 0) * 100

        return {
            "score": round(score, 2),
            "explanation": f"Price agreement status: {price_agreement.get('status', 'Unknown')}.",
        }

    def _score_macro_context(self, company_overview):
        macro_confidence = company_overview.confidence.get("macro_context")

        score = macro_confidence.score * 100 if macro_confidence else 0

        return {
            "score": round(score, 2),
            "explanation": (
                macro_confidence.explanation
                if macro_confidence
                else "No macroeconomic context available."
            ),
        }

    def _score_company_identity(self, company_overview):
        company_confidence = company_overview.confidence.get("company_profile")

        score = company_confidence.score * 100 if company_confidence else 0

        return {
            "score": round(score, 2),
            "explanation": (
                company_confidence.explanation
                if company_confidence
                else "Company identity could not be verified."
            ),
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