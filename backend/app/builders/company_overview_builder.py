from app.models.company import CompanyOverview


class CompanyOverviewBuilder:
    def build(
        self,
        ticker,
        fmp_profile,
        finnhub_profile,
        alpha_vantage_quote,
        sec_company,
        fundamentals,
        macro_snapshot,
        confidence,
        agreement,
    ):
        return CompanyOverview(
            ticker=ticker,
            company=(
                (fmp_profile or {}).get("companyName")
                or (finnhub_profile or {}).get("name")
                or (sec_company or {}).get("company")
                or (alpha_vantage_quote or {}).get("symbol")
            ),
            price=(
                (fmp_profile or {}).get("price")
                or (alpha_vantage_quote or {}).get("price")
            ),
            market_cap=(
                (fmp_profile or {}).get("marketCap")
                or (fmp_profile or {}).get("mktCap")
                or (finnhub_profile or {}).get("marketCapitalization")
            ),
            sector=(fmp_profile or {}).get("sector"),
            industry=(
                (fmp_profile or {}).get("industry")
                or (finnhub_profile or {}).get("finnhubIndustry")
            ),
            website=(
                (fmp_profile or {}).get("website")
                or (finnhub_profile or {}).get("weburl")
            ),
            summary=(fmp_profile or {}).get("description"),
            fundamentals=fundamentals,
            sources={
                "fmp_profile": fmp_profile is not None,
                "fmp_key_metrics_ttm": fundamentals is not None,
                "fmp_ratios_ttm": fundamentals is not None,
                "fmp_financial_growth": fundamentals is not None,
                "finnhub_profile": finnhub_profile is not None,
                "alpha_vantage_quote": alpha_vantage_quote is not None,
                "sec_company": sec_company is not None,
                "fred_macro": macro_snapshot is not None,
            },
            confidence=confidence,
            agreement=agreement,
            score={},
            status="company_overview_builder_v1",
        )