def review_status(
    confidence: float,
    has_evidence: bool = True,
) -> str:

    if not has_evidence:
        return "needs_review"

    if confidence >= 0.90:
        return "accepted"

    if confidence >= 0.70:
        return "needs_review"

    return "unresolved"


def should_review(
    confidence: float,
    has_evidence: bool = True,
) -> bool:

    return review_status(
        confidence,
        has_evidence,
    ) != "accepted"