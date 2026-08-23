import pandas as pd

from src.lov_profile import (
    profile_dataframe,
)


def test_profile_detects_taxonomy():

    df = pd.DataFrame({
        "Classpath": [
            "Abrasives > Cut-Off Discs",
            "Appliances > Dishwashers",
        ]
    })

    profile = profile_dataframe(df)

    assert len(profile.taxonomy_paths) == 2


def test_profile_detects_attributes():

    df = pd.DataFrame({
        "Classpath": [
            "Abrasives > Cut-Off Discs",
        ],
        "Attribute Label": [
            "Diameter",
        ],
        "Attribute Values": [
            "4 in, 4-1/2 in, 5 in",
        ],
    })

    profile = profile_dataframe(df)

    assert "Diameter" in profile.attribute_labels

    assert "4 in" in profile.attribute_values[
        "Diameter"
    ]


def test_profile_summary():

    df = pd.DataFrame({
        "Attribute Label": [
            "Diameter",
            "Material",
        ],
        "Attribute Values": [
            "4 in, 5 in",
            "Steel, Aluminum",
        ],
    })

    profile = profile_dataframe(df)

    summary = profile.summary()

    assert summary["attribute_count"] == 2
    assert summary["controlled_value_count"] == 4

