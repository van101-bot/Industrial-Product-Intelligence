from src.taxonomy import load_lov
from src.normalizer import (
    normalize_number,
    normalize_pack_quantity,
)


def test_lov_can_be_loaded():

    df = load_lov()

    print("\n=== LOV PROFILE ===")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))

    print("\n=== SAMPLE ===")
    print(df.head(10).to_string())

    assert len(df) > 0
    assert len(df.columns) > 0


def test_fraction_normalization():

    assert normalize_number("7/8") == 0.875
    assert normalize_number("4.5") == 4.5


def test_pack_quantity():

    assert normalize_pack_quantity("50") == 50