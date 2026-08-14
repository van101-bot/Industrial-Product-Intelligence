from src.sources.models import SearchResult


MARKETPLACE_DOMAINS = {
    "amazon.com",
    "ebay.com",
}


def classify_source(
    result: SearchResult,
    manufacturer_domain: str | None = None,
) -> SearchResult:
    """
    Rank a search result according to source reliability.

    Manufacturer domains are preferred.
    Known marketplaces are downgraded.
    """

    domain = result.domain.lower().strip()

    score = 0.0
    source_type = "secondary"
    reason = "Secondary source"

    if manufacturer_domain:
        expected_domain = manufacturer_domain.lower().strip()

        if expected_domain in domain:
            score += 1.0
            source_type = "manufacturer"
            reason = "Matches supplied manufacturer domain"

    if domain in MARKETPLACE_DOMAINS:
        score -= 1.0
        source_type = "marketplace"
        reason = "Known marketplace source"

    result.score = score
    result.source_type = source_type
    result.reason = reason

    return result