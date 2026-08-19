SOURCE_PRIORITY = {
    "source_data": 1.00,
    "company_lov": 0.95,
    "manufacturer_master": 0.90,
    "description_extraction": 0.75,
    "taxonomy_rule": 0.70,
    "derived": 0.60,
    "fallback": 0.30,
}


def provenance_confidence(source: str) -> float:
    return SOURCE_PRIORITY.get(source, 0.0)


def make_provenance(
    value,
    source: str,
    evidence: str | None = None,
) -> dict:

    return {
        "value": value,
        "source": source,
        "confidence": provenance_confidence(source),
        "evidence": evidence,
    }