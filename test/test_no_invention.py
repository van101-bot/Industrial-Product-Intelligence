from src.attributes import AttributeEnricher


def test_missing_attributes_are_not_invented(monkeypatch):

    text = """
    Generic Metal Cut-Off Disc
    """

    fake_result = {
        "raw": {
            "product_type": "Metal Cut-Off Disc",
            "brand": None,
            "diameter": None,
            "thickness": None,
            "arbor": None,
        },
        "normalized": {
            "product_type": "Metal Cut-Off Disc",
            "brand": None,
            "diameter": None,
            "thickness": None,
            "arbor": None,
        },
    }

    def fake_extract_product_attributes(self, text):
        return fake_result

    monkeypatch.setattr(
        "src.attributes.GeminiAIExtractor.extract_product_attributes",
        fake_extract_product_attributes,
    )

    enricher = AttributeEnricher()

    result = enricher.enrich(text)

    attributes = result["normalized"]

    assert attributes.get("diameter") is None
    assert attributes.get("thickness") is None
    assert attributes.get("arbor") is None