class PeerRules:
    PEER_GROUPS = {
        "AAPL": ["MSFT", "GOOGL", "DELL", "HPQ", "SONY"],
        "MSFT": ["AAPL", "GOOGL", "ORCL", "ADBE", "CRM"],
        "GOOGL": ["META", "MSFT", "AAPL", "AMZN", "NFLX"],
        "NVDA": ["AMD", "AVGO", "QCOM", "MRVL", "INTC"],
        "AMD": ["NVDA", "INTC", "QCOM", "AVGO", "MRVL"],
        "TSLA": ["GM", "F", "RIVN", "LCID", "TM"],
        "JPM": ["BAC", "WFC", "C", "GS", "MS"],
        "BAC": ["JPM", "WFC", "C", "GS", "MS"],
        "AMZN": ["WMT", "TGT", "COST", "BABA", "EBAY"],
        "META": ["GOOGL", "SNAP", "PINS", "NFLX", "AAPL"],
    }

    def get_peers(self, ticker: str):
        clean_ticker = ticker.upper()
        return self.PEER_GROUPS.get(clean_ticker, [])