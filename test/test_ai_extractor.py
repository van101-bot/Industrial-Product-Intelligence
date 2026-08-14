from src.ai_extractor import MockAIExtractor


def test_ai_extractor_returns_structured_attributes():

    evidence = """
    4-1/2" x .045" x 7/8"
    Performance+ Metal Cut Off Wheel - Type 27
    Maximum RPM: 13,300 RPM
    """

    extractor = MockAIExtractor()

    result = extractor.extract(evidence)

    assert result.product_type == "Metal Cut-Off Wheel"
    assert result.series == "Performance+"
    assert result.diameter == "4-1/2 in"
    assert result.thickness == "0.045 in"
    assert result.arbor_size == "7/8 in"
    assert result.wheel_type == "Type 27"
    assert result.max_rpm == "13,300 RPM"


def test_ai_extractor_does_not_invent_missing_fields():

    evidence = """
    Performance+ Metal Cut Off Wheel
    """

    extractor = MockAIExtractor()

    result = extractor.extract(evidence)

    assert result.series == "Performance+"
    assert result.product_type == "Metal Cut-Off Wheel"

    assert result.diameter is None
    assert result.thickness is None
    assert result.arbor_size is None
    assert result.wheel_type is None
    assert result.max_rpm is None