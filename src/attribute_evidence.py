def build_attribute_evidence(raw: dict, normalized: dict) -> list:
    """
    Build evidence linking each normalized attribute back
    to the original extracted value.

    Missing attributes are ignored.
    """

    evidence = []

    for attribute, raw_value in raw.items():

        # No evidence if the AI did not extract a value
        if raw_value is None:
            continue

        normalized_value = normalized.get(attribute)

        # Do not create evidence for values that failed normalization
        if normalized_value is None:
            continue

        evidence.append({
            "attribute": attribute,
            "raw_value": raw_value,
            "normalized_value": normalized_value,
            "source": "ai_extraction",
        })

    return evidence