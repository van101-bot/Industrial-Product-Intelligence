def decide_status(
    confidence: float,
    evidence_count: int,
    unresolved_fields: int,
) -> str:

    if confidence >= 0.85 and evidence_count >= 1:
        return "accepted"

    if confidence >= 0.60:
        return "review"

    if unresolved_fields > 0:
        return "unresolved"

    return "review"