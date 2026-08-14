from typing import Any


def normalize_value(value: Any) -> str:
    """
    Normalize values for comparison.
    """

    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .lower()
        .replace("″", '"')
        .replace("inches", "in")
    )


def validate_fact(
    field: str,
    ai_value: Any,
    extracted_value: Any,
) -> dict:
    """
    Compare an AI/external value against an independently
    extracted value.
    """

    ai_normalized = normalize_value(ai_value)
    extracted_normalized = normalize_value(extracted_value)

    if not ai_normalized:
        return {
            "field": field,
            "value": extracted_value,
            "status": "missing_ai_value",
            "confidence": 0.8,
            "needs_review": False,
        }

    if not extracted_normalized:
        return {
            "field": field,
            "value": ai_value,
            "status": "no_independent_evidence",
            "confidence": 0.4,
            "needs_review": True,
        }

    if ai_normalized == extracted_normalized:
        return {
            "field": field,
            "value": ai_value,
            "status": "validated",
            "confidence": 0.99,
            "needs_review": False,
        }

    return {
        "field": field,
        "value": ai_value,
        "status": "conflict",
        "confidence": 0.1,
        "needs_review": True,
        "independent_value": extracted_value,
    }