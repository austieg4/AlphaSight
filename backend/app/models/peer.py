from pydantic import BaseModel


class PeerGroup(BaseModel):
    ticker: str
    peers: list[str]
    peer_count: int
    status: str