from app.intelligence.industry_rules import IndustryRules


class ValuationScoreEngine:
    def __init__(self):
        self.industry_rules = IndustryRules()

    def calculate(self, fundamentals, industry=None):
        if not fundamentals:
            return {"score": 0, "explanation": "No valuation fundamentals available."}

        rules = self.industry_rules.get_rules_for_industry(industry)
        valuation_rules = rules["valuation"]

        score = 0
        checks = 0

        metric_map = {
            "pe_ratio": fundamentals.pe_ratio,
            "price_to_sales": fundamentals.price_to_sales,
            "price_to_book": fundamentals.price_to_book,
        }

        for metric_name, value in metric_map.items():
            if value is None:
                continue

            checks += 1
            thresholds = valuation_rules[metric_name]

            if value <= thresholds["excellent"]:
                score += 100
            elif value <= thresholds["good"]:
                score += 75
            elif value <= thresholds["fair"]:
                score += 50
            else:
                score += 25

        if checks == 0:
            return {"score": 0, "explanation": "No valuation metrics available."}

        return {
            "score": round(score / checks, 2),
            "explanation": (
                f"Valuation score based on {checks} metrics "
                f"using {industry or 'default'} industry rules."
            ),
        }
        