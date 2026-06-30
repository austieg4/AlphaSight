from app.intelligence.peer_rules import PeerRules


class PeerIntelligence:
    def __init__(self):
        self.peer_rules = PeerRules()

    def get_peer_summary(self, ticker: str):
        peers = self.peer_rules.get_peers(ticker)

        return {
            "ticker": ticker.upper(),
            "peers": peers,
            "peer_count": len(peers),
            "status": "static_peer_group_v1",
        }