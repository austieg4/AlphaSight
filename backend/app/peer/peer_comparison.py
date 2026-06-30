from statistics import mean

from app.models.peer_analysis import PeerMetricComparison


class PeerComparisonEngine:
    """
    Compares a company against a collection of peer snapshots.
    """

    POSITIVE_ONLY_METRICS = {
        "pe_ratio",
        "price_to_sales",
        "price_to_book",
        "market_cap",
        "overall_score",
    }

    def compare_metric(self, company_snapshot, peer_snapshots, metric_name):
        company_value = getattr(company_snapshot, metric_name, None)

        if company_value is None:
            return None

        if metric_name in self.POSITIVE_ONLY_METRICS and company_value <= 0:
            return None

        peer_values = []

        for peer in peer_snapshots:
            value = getattr(peer, metric_name, None)

            if value is None:
                continue

            if (
                metric_name in self.POSITIVE_ONLY_METRICS
                and value <= 0
            ):
                continue

            peer_values.append(value)

        if not peer_values:
            return None

        peer_average = mean(peer_values)

        if peer_average == 0:
            return None

        difference_percent = (
            (company_value - peer_average)
            / peer_average
        ) * 100

        if abs(difference_percent) <= 10:
            assessment = "Near Peer Average"
        elif difference_percent > 0:
            assessment = "Above Peer Average"
        else:
            assessment = "Below Peer Average"

        return PeerMetricComparison(
            metric=metric_name,
            company_value=round(company_value, 2),
            peer_average=round(peer_average, 2),
            difference_percent=round(difference_percent, 2),
            assessment=assessment,
        )