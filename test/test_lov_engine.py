import pandas as pd

from src.lov_profile import profile_dataframe
from src.lov_engine import LOVEngine


def build_engine():

    df = pd.DataFrame({
        "Classpath": [
            "Abrasives > Cut-Off Discs",
            "Appliances > Dishwashers",
        ],
        "Attribute Label": [
            "Material",
            "Material",
        ],
        "Attribute Values": [
            "Steel, Aluminum",
            "Stainless Steel, Plastic",
        ],
    })

    profile = profile_dataframe(df)

    return LOVEngine(profile)


def test_taxonomy_uses_company_lov():

    engine = build_engine()

    result = engine.classify(
        "4-1/2 inch steel cut off disc"
    )

    assert result["category"] == (
        "Abrasives > Cut-Off Discs"
    )

    assert result["source"] == "company_lov"


def test_exact_attribute_value():

    engine = build_engine()

    result = engine.normalize_attribute(
        "Material",
        "Steel",
    )

    assert result["value"] == "Steel"

    assert result["confidence"] == 1.0


def test_unknown_attribute_value_not_invented():

    engine = build_engine()

    result = engine.normalize_attribute(
        "Material",
        "Titanium",
    )

    assert result["value"] is None


def test_validation():

    engine = build_engine()

    result = engine.validate_attribute(
        "Material",
        "Steel",
    )

    assert result["valid"] is True


def test_invalid_value():

    engine = build_engine()

    result = engine.validate_attribute(
        "Material",
        "Titanium",
    )

    assert result["valid"] is False

