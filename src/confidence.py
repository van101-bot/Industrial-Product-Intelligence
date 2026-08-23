def calculate_field_confidence(
    source: str,
    evidence_present: bool,
    controlled_value: bool = False,
) -> float:

    if controlled_value and evidence_present:
        return 1.0

    if source == "source_data" and evidence_present:
        return 0.98

    if source == "company_lov" and evidence_present:
        return 0.95

    if source == "manufacturer_master" and evidence_present:
        return 0.90

    if source == "description_extraction" and evidence_present:
        return 0.80

    if source == "derived":
        return 0.60

    return 0.0

def calculate_confidence(
    field_confidences: dict,
    evidence_count: int = 0,
    unresolved_count: int = 0,
) -> float:

    values = [
        float(v)
        for v in field_confidences.values()
        if v is not None
    ]

    if not values:
        base = 0.0
    else:
        base = sum(values) / len(values)

    evidence_bonus = min(
        evidence_count * 0.03,
        0.10
    )

    unresolved_penalty = min(
        unresolved_count * 0.05,
        0.25
    )

    score = (
        base
        + evidence_bonus
        - unresolved_penalty
    )

    return round(
        max(0.0, min(1.0, score)),
        3
    )


def confidence_band(score: float) -> str:

    if score >= 0.85:
        return "high"

    if score >= 0.65:
        return "medium"

    return "low"