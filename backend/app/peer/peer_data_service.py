import asyncio

from app.peer.peer_models import PeerSnapshot


class PeerDataService:
    """
    Builds normalized peer snapshots from AlphaSight company overviews.
    """

    def build_snapshot(self, company_overview):
        fundamentals = company_overview.fundamentals

        return PeerSnapshot(
            ticker=company_overview.ticker,
            company=company_overview.company,
            industry=company_overview.industry,
            price=company_overview.price,
            market_cap=company_overview.market_cap,
            pe_ratio=fundamentals.pe_ratio if fundamentals else None,
            price_to_sales=fundamentals.price_to_sales if fundamentals else None,
            price_to_book=fundamentals.price_to_book if fundamentals else None,
            revenue_growth=fundamentals.revenue_growth if fundamentals else None,
            net_income_growth=fundamentals.net_income_growth if fundamentals else None,
            gross_margin=fundamentals.gross_margin if fundamentals else None,
            operating_margin=fundamentals.operating_margin if fundamentals else None,
            return_on_equity=fundamentals.return_on_equity if fundamentals else None,
            overall_score=(
                company_overview.score.overall_score
                if company_overview.score
                else None
            ),
        )

    async def build_peer_snapshots(
        self,
        peer_tickers,
        market_data_service,
    ):
        results = await asyncio.gather(
            *[
                market_data_service.get_company_overview(ticker)
                for ticker in peer_tickers
            ],
            return_exceptions=True,
        )

        snapshots = []

        for result in results:
            if isinstance(result, Exception) or result is None:
                continue

            snapshots.append(self.build_snapshot(result))

        return snapshots