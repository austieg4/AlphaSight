from typing import Optional

from pydantic import BaseModel


class CompanyFundamentals(BaseModel):
    pe_ratio: Optional[float] = None
    price_to_sales: Optional[float] = None
    price_to_book: Optional[float] = None
    ev_to_ebitda: Optional[float] = None

    current_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None

    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    return_on_equity: Optional[float] = None
    return_on_assets: Optional[float] = None

    revenue_per_share: Optional[float] = None
    net_income_per_share: Optional[float] = None
    free_cash_flow_per_share: Optional[float] = None
    cash_per_share: Optional[float] = None
    book_value_per_share: Optional[float] = None

    revenue_growth: Optional[float] = None
    gross_profit_growth: Optional[float] = None
    operating_income_growth: Optional[float] = None
    net_income_growth: Optional[float] = None
    eps_growth: Optional[float] = None
    free_cash_flow_growth: Optional[float] = None