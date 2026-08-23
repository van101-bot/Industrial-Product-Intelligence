from src.taxonomy_classifier import classify_product


def test_cutoff_disc_taxonomy():

    result = classify_product(
        '4-1/2"x.045"x7/8" '
        "Performance+ Metal Cut Off Disc"
    )

    assert result["category"] == (
        "Abrasives > Cut-Off Discs"
    )


def test_sanding_belt_taxonomy():

    result = classify_product(
        'DCB518ASTS06G Diablo 1/2"x18" - Sanding Belt 6pc'
    )

    assert result["category"] == (
        "Abrasives > Sanding Belts"
    )


def test_unknown_product_is_not_invented():

    result = classify_product(
        "Generic Product With No Known Category"
    )

    assert result["category"] is None

def test_taxonomy_returns_none_for_unknown():
    result = classify_product(
        "Completely Unknown Industrial Thing"
    )

    assert result["category"] is None

def test_taxonomy_confidence_matches_classification():
    result = classify_product(
        '4-1/2"x.045"x7/8" Performance+ Metal Cut Off Disc'
    )

    assert result["category"] == "Abrasives > Cut-Off Discs"
    assert result["confidence"] > 0

def test_decking_taxonomy():

    result = classify_product(
        "1x6-16' Coastline Square Edge Vintage Azek PVC Decking"
    )

    assert result["category"] == (
        "Building Materials > Decking"
    )


def test_rail_taxonomy():

    result = classify_product(
        "6' White Select T-Rail Kit Horizontal"
    )

    assert result["category"] == (
        "Building Materials > Rail Kits"
    )


def test_tire_pressure_taxonomy():

    result = classify_product(
        "Digital Tire Pressure Inflator Gauge"
    )

    assert result["category"] == (
        "Automotive > Tire Pressure Gauges"
    )


def test_unknown_taxonomy_is_not_invented():

    result = classify_product(
        "Completely Unknown Industrial Object XYZ"
    )

    assert result["category"] is None

def test_unknown_value_is_rejected():

    result = classify_product(
        "Industrial Component UnknownXYZ"
    )

    assert result["category"] is None

