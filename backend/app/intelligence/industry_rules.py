class IndustryRules:
    DEFAULT_RULES = {
        "valuation": {
            "pe_ratio": {
                "excellent": 15,
                "good": 25,
                "fair": 40,
            },
            "price_to_sales": {
                "excellent": 3,
                "good": 7,
                "fair": 12,
            },
            "price_to_book": {
                "excellent": 3,
                "good": 8,
                "fair": 15,
            },
        }
    }

    INDUSTRY_RULES = {
        "Consumer Electronics": {
            "valuation": {
                "pe_ratio": {
                    "excellent": 25,
                    "good": 35,
                    "fair": 45,
                },
                "price_to_sales": {
                    "excellent": 5,
                    "good": 10,
                    "fair": 15,
                },
                "price_to_book": {
                    "excellent": 10,
                    "good": 25,
                    "fair": 45,
                },
            }
        },
        "Semiconductors": {
            "valuation": {
                "pe_ratio": {
                    "excellent": 25,
                    "good": 40,
                    "fair": 60,
                },
                "price_to_sales": {
                    "excellent": 8,
                    "good": 15,
                    "fair": 25,
                },
                "price_to_book": {
                    "excellent": 8,
                    "good": 20,
                    "fair": 35,
                },
            }
        },
        "Banks - Diversified": {
            "valuation": {
                "pe_ratio": {
                    "excellent": 10,
                    "good": 15,
                    "fair": 20,
                },
                "price_to_sales": {
                    "excellent": 2,
                    "good": 4,
                    "fair": 6,
                },
                "price_to_book": {
                    "excellent": 1,
                    "good": 1.8,
                    "fair": 3,
                },
            }
        },
    }

    def get_rules_for_industry(self, industry):
        if not industry:
            return self.DEFAULT_RULES

        return self.INDUSTRY_RULES.get(industry, self.DEFAULT_RULES)