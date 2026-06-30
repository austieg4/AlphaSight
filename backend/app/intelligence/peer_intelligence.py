from app.intelligence.peer_rules import PeerRules
from app.models.peer import PeerGroup


class PeerIntelligence:
    def __init__(self):
        self.peer_rules = PeerRules()

    def get_peer_summary(self, ticker: str):
        peers = self.peer_rules.get_peers(ticker)

        return PeerGroup(
            ticker=ticker.upper(),
            peers=peers,
            peer_count=len(peers),
            status="typed_peer_group_v1",
        )