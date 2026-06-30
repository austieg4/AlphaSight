from statistics import mean


class PeerComparisonEngine:
    """
    Compares a company against a collection of peer snapshots.
    """

    def compare_metric(self, company_snapshot, peer_snapshots, metric_name):
        company_value = getattr(company_snapshot, metric_name, None)

        peer_values = [
            getattr(peer, metric_name)
            for peer in peer_snapshots
            if getattr(peer, metric_name) is not None
        ]

        if company_value is None or not peer_values:
            return None

        peer_average = mean(peer_values)

        difference_percent = (
            (company_value - peer_average)
            / peer_average
            * 100
        ) if peer_average else 0

        if abs(difference_percent) <= 10:
            assessment = "Near Peer Average"
        elif difference_percent > 0:
            assessment = "Above Peer Average"
        else:
            assessment = "Below Peer Average"

        return {
            "metric": metric_name,
            "company_value": round(company_value, 2),
            "peer_average": round(peer_average, 2),
            "difference_percent": round(difference_percent, 2),
            "assessment": assessment,
        }