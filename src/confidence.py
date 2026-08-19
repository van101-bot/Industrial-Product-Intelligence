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