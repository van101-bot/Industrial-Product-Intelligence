from src.entity_resolver import (
    resolve_manufacturer,
    resolve_brand,
)


def test_milwaukee_manufacturer_resolution():

    result = resolve_manufacturer(
        "Milwaukee Accessory"
    )

    print("\n=== MILWAUKEE RESOLUTION ===")
    print(result)

    assert result["value"] is not None
    assert result["score"] >= 75


def test_diablo_brand_resolution():

    result = resolve_brand("Diablo")

    print("\n=== DIABLO RESOLUTION ===")
    print(result)

    assert result["value"] is not None
    assert result["score"] >= 75