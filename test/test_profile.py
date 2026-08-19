import pandas as pd
from pathlib import Path


from src.lov_profile import load_lov_profile
from src.profile import (
    clean_dataframe,
    detect_taxonomy_columns,
    detect_attribute_columns,
    load_lov_profile,
)

def load_profile(path):
    """
    Public profile-loading entry point.
    """
    return load_lov_profile(path)


def test_placeholder_values_are_removed():

    df = pd.DataFrame({
        "Brand": [
            "3M",
            "-- Unbranded --",
            "",
            None,
        ]
    })

    cleaned = clean_dataframe(df)

    # Real value must remain unchanged
    assert cleaned.loc[0, "Brand"] == "3M"

    # Placeholder values must become missing
    assert str(cleaned.loc[1, "Brand"]).lower() in ("nan", "none", "")
    assert str(cleaned.loc[2, "Brand"]).lower() in ("nan", "none", "")
    assert str(cleaned.loc[3, "Brand"]).lower() in ("nan", "none", "")


def test_taxonomy_columns_are_detected():

    columns = [
        "Classpath",
        "Attribute Label",
        "Brand",
        "Department",
    ]

    result = detect_taxonomy_columns(columns)

    assert "Classpath" in result
    assert "Department" in result


def test_attribute_columns_are_detected():

    columns = [
        "Classpath",
        "Attribute Label",
        "Attribute Values",
        "Brand",
    ]

    result = detect_attribute_columns(columns)

    assert "Attribute Label" in result
    assert "Attribute Values" in result



from src.profile import (
    load_table,
    build_profile,
)


def test_csv_can_be_loaded():

    path = Path(
        "data/raw/Unihack_ Sample Dataset - Input.csv"
    )

    if not path.exists():
        path = Path(
            "data/Unihack_ Sample Dataset - Input.csv"
        )

    assert path.exists()

    df = load_table(path)

    assert len(df) == 1000
    assert "Part_Desc" in df.columns
    assert "Part_Manuf" in df.columns


def test_profile_can_be_built_from_csv():

    path = Path(
        "data/raw/Unihack_ Sample Dataset - Input.csv"
    )

    if not path.exists():
        path = Path(
            "data/Unihack_ Sample Dataset - Input.csv"
        )

    assert path.exists()

    profile = build_profile(path)

    assert profile["format"] == "csv"
    assert "default" in profile["sheets"]
    assert profile["sheets"]["default"]["rows"] == 1000

def test_company_lov_profile_has_taxonomy():
    from src.profile import load_profile

    profile = load_profile(
        "data/demo/company_lov.csv"
    )

    assert profile["taxonomy_count"] > 0

def test_company_lov_has_controlled_values():
    from src.profile import load_profile

    profile = load_profile(
        "data/demo/company_lov.csv"
    )

    assert profile["controlled_value_count"] > 0