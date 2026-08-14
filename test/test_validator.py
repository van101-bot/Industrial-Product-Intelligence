from src.validator import validate_fact


def test_matching_values_are_validated():

    result = validate_fact(
        "diameter",
        "4-1/2 in",
        "4-1/2 in",
    )

    assert result["status"] == "validated"
    assert result["confidence"] == 0.99
    assert result["needs_review"] is False


def test_conflicting_values_require_review():

    result = validate_fact(
        "diameter",
        "5 in",
        "4-1/2 in",
    )

    assert result["status"] == "conflict"
    assert result["needs_review"] is True
    assert result["independent_value"] == "4-1/2 in"