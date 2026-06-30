from app.models.fundamentals import CompanyFundamentals


class FundamentalsBuilder:
    def build(self, key_metrics, ratios, growth):
        if key_metrics is None and ratios is None and growth is None:
            return None

        key_metrics = key_metrics or {}
        ratios = ratios or {}
        growth = growth or {}

        return CompanyFundamentals(
            pe_ratio=(
                key_metrics.get("priceToEarningsRatioTTM")
                or ratios.get("priceToEarningsRatioTTM")
            ),
            price_to_sales=(
                key_metrics.get("priceToSalesRatioTTM")
                or ratios.get("priceToSalesRatioTTM")
            ),
            price_to_book=(
                key_metrics.get("priceToBookRatioTTM")
                or ratios.get("priceToBookRatioTTM")
            ),
            ev_to_ebitda=(
                key_metrics.get("enterpriseValueMultipleTTM")
                or ratios.get("enterpriseValueMultipleTTM")
            ),
            current_ratio=(
                key_metrics.get("currentRatioTTM")
                or ratios.get("currentRatioTTM")
            ),
            debt_to_equity=(
                key_metrics.get("debtToEquityRatioTTM")
                or ratios.get("debtToEquityRatioTTM")
            ),
            gross_margin=(
                key_metrics.get("grossProfitMarginTTM")
                or ratios.get("grossProfitMarginTTM")
            ),
            operating_margin=(
                key_metrics.get("operatingProfitMarginTTM")
                or ratios.get("operatingProfitMarginTTM")
            ),
            net_margin=(
                key_metrics.get("netProfitMarginTTM")
                or ratios.get("netProfitMarginTTM")
            ),
            return_on_equity=(
                key_metrics.get("returnOnEquityTTM")
                or ratios.get("returnOnEquityTTM")
            ),
            return_on_assets=(
                key_metrics.get("returnOnAssetsTTM")
                or ratios.get("returnOnAssetsTTM")
            ),
            revenue_per_share=(
                key_metrics.get("revenuePerShareTTM")
                or ratios.get("revenuePerShareTTM")
            ),
            net_income_per_share=(
                key_metrics.get("netIncomePerShareTTM")
                or ratios.get("netIncomePerShareTTM")
            ),
            free_cash_flow_per_share=(
                key_metrics.get("freeCashFlowPerShareTTM")
                or ratios.get("freeCashFlowPerShareTTM")
            ),
            cash_per_share=(
                key_metrics.get("cashPerShareTTM")
                or ratios.get("cashPerShareTTM")
            ),
            book_value_per_share=(
                key_metrics.get("bookValuePerShareTTM")
                or ratios.get("bookValuePerShareTTM")
            ),
            revenue_growth=growth.get("revenueGrowth"),
            gross_profit_growth=growth.get("grossProfitGrowth"),
            operating_income_growth=growth.get("operatingIncomeGrowth"),
            net_income_growth=growth.get("netIncomeGrowth"),
            eps_growth=growth.get("epsgrowth"),
            free_cash_flow_growth=growth.get("freeCashFlowGrowth"),
        )