from app.peer.peer_comparison import PeerComparisonEngine
from app.peer.peer_models import PeerSnapshot


def test_compare_metric_above_peer_average():
    company = PeerSnapshot(
        ticker="AAPL",
        pe_ratio=35.0,
    )

    peers = [
        PeerSnapshot(ticker="MSFT", pe_ratio=30.0),
        PeerSnapshot(ticker="GOOGL", pe_ratio=28.0),
        PeerSnapshot(ticker="SONY", pe_ratio=32.0),
    ]

    engine = PeerComparisonEngine()
    result = engine.compare_metric(company, peers, "pe_ratio")

    assert result["metric"] == "pe_ratio"
    assert result["company_value"] == 35.0
    assert result["peer_average"] == 30.0
    assert result["difference_percent"] == 16.67
    assert result["assessment"] == "Above Peer Average"


def test_compare_metric_returns_none_when_company_value_missing():
    company = PeerSnapshot(ticker="AAPL")

    peers = [
        PeerSnapshot(ticker="MSFT", pe_ratio=30.0),
    ]

    engine = PeerComparisonEngine()
    result = engine.compare_metric(company, peers, "pe_ratio")

    assert result is None


def test_compare_metric_returns_none_when_peer_values_missing():
    company = PeerSnapshot(
        ticker="AAPL",
        pe_ratio=35.0,
    )

    peers = [
        PeerSnapshot(ticker="MSFT"),
        PeerSnapshot(ticker="GOOGL"),
    ]

    engine = PeerComparisonEngine()
    result = engine.compare_metric(company, peers, "pe_ratio")

    assert result is None