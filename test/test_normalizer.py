from src.normalizer import (
    normalize_number,
    normalize_pack_quantity,
    normalize_grit,
    normalize_attribute_record,
)


def test_decimal_normalization():
    assert normalize_number("4.5") == 4.5


def test_fraction_normalization():
    assert normalize_number("7/8") == 0.875


def test_mixed_fraction_normalization():
    assert normalize_number("4 1/2") == 4.5


def test_inch_symbol_normalization():
    assert normalize_number('4-1/2"') == 4.5
    assert normalize_number('4.5"') == 4.5
    assert normalize_number('.045"') == 0.045


def test_pack_quantity():
    assert normalize_pack_quantity("10pc") == 10
    assert normalize_pack_quantity("50 pcs") == 50
    assert normalize_pack_quantity("100 pieces") == 100


def test_grit_normalization():
    assert normalize_grit("P150") == "P150"
    assert normalize_grit("p 150") == "P150"
    assert normalize_grit("150") == "P150"


def test_missing_values_are_not_invented():
    result = normalize_attribute_record({
        "diameter": None,
        "thickness": None,
        "arbor": None,
        "grit": None,
    })
    assert result["diameter"] is None
    assert result["thickness"] is None
    assert result["arbor"] is None
    assert result["grit"] is None


def test_realistic_cutoff_disc():
    result = normalize_attribute_record({
        "product_type": "Metal Cut Off Disc",
        "diameter": '4.5"',
        "thickness": '.045"',
        "arbor": "7/8",
        "grit": "P150",
        "pack_quantity": "10pc",
    })
    assert result["diameter"] == 4.5
    assert result["thickness"] == 0.045
    assert result["arbor"] == 0.875
    assert result["grit"] == "P150"
    assert result["pack_quantity"] == 10
