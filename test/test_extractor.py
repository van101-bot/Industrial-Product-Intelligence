from src.extractor import extract_product_facts


def test_extract_product_facts():

    text = """
    4-1/2" x .045" x 7/8"
    Performance+ Metal Cut Off Wheel - Type 27

    Maximum RPM: 13,300 RPM
    """

    facts = extract_product_facts(text)

    assert facts["diameter"] == "4-1/2 in"
    assert facts["thickness"] == ".045 in"
    assert facts["arbor"] == "7/8 in"
    assert facts["wheel_type"] == "Type 27"
    assert facts["max_rpm"] == "13,300 RPM"