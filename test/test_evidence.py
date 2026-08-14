from src.evidence import Evidence


def test_evidence_structure():

    evidence = Evidence(
        field="diameter",
        value="4-1/2 in",
        source_url="https://example.com/product",
        source_type="manufacturer",
        confidence=0.97,
        excerpt="4-1/2 in diameter",
    )

    result = evidence.to_dict()

    assert result["field"] == "diameter"
    assert result["value"] == "4-1/2 in"
    assert result["source_type"] == "manufacturer"
    assert result["confidence"] == 0.97