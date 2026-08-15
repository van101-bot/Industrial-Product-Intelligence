from src.attribute_evidence import build_attribute_evidence


def test_attribute_evidence_is_created():

    raw = {
        "diameter": "4-1/2",
        "thickness": ".045",
        "arbor": "7/8",
    }

    normalized = {
        "diameter": 4.5,
        "thickness": 0.045,
        "arbor": 0.875,
    }

    evidence = build_attribute_evidence(
        raw,
        normalized,
    )

    assert len(evidence) == 3

    assert evidence[0]["attribute"] == "diameter"
    assert evidence[0]["raw_value"] == "4-1/2"
    assert evidence[0]["normalized_value"] == 4.5


def test_missing_attributes_have_no_evidence():

    raw = {
        "diameter": "4-1/2",
        "thickness": None,
    }

    normalized = {
        "diameter": 4.5,
        "thickness": None,
    }

    evidence = build_attribute_evidence(
        raw,
        normalized,
    )

    assert len(evidence) == 1
    assert evidence[0]["attribute"] == "diameter"