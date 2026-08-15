from src.normalizer import (
    normalize_number,
    normalize_pack_quantity,
    normalize_attribute_record,
)


def test_dimension_normalization():

    result = normalize_attribute_record({
        "diameter": "4.5",
        "thickness": ".045",
        "arbor": "7/8",
    })

    assert result["diameter"] == 4.5
    assert result["thickness"] == 0.045
    assert result["arbor"] == 0.875


def test_abrasive_grade_is_preserved():

    result = normalize_attribute_record({
        "abrasive_grade": "P150",
    })

    assert result["abrasive_grade"] == "P150"


def test_pack_quantity():

    result = normalize_attribute_record({
        "pack_quantity": "50",
    })

    assert result["pack_quantity"] == 50


def test_missing_attributes_remain_missing():

    result = normalize_attribute_record({
        "diameter": None,
        "thickness": None,
        "arbor": None,
    })

    assert result["diameter"] is None
    assert result["thickness"] is None
    assert result["arbor"] is None